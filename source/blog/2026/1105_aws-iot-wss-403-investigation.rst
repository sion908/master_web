AWS IoT CoreのWebSocket接続で403が続いた原因を切り分ける
==========================================================

.. post:: 2026-11-05
   :tags: AWS, 個人開発, 運用
   :author: sion908
   :language: ja
   :location: blog/2026

.. meta::
   :description: AWS IoT CoreへのMQTT over WebSocket接続で403が続いた。SigV4のセッショントークンとCognito IdentityへのIoTポリシー未アタッチを、HTTP応答とMQTT接続の観測で切り分けた記録。


ブラウザからAWS IoT Coreの状態トピックを購読しようとしたところ、WebSocket接続がHTTP 403で失敗した。認証済みユーザーを替えても、管理者権限のクレデンシャルで試しても同じだった。一方、画面はRESTポーリングに切り替わるため、機能自体は動いているように見える。

今回の環境には問題が二つあった。SigV4の署名計算に一時クレデンシャルのセッショントークンを含めていたことと、認証済みCognito IdentityにIoTポリシーをアタッチしていなかったことだ。署名を直すとWebSocketのupgradeが通り、ポリシーをアタッチするとMQTTの購読と受信まで通った。


構成と最初の症状
----------------

ブラウザのSPAでCognito User Poolへログインし、Identity Poolから一時的なAWSクレデンシャルを取得する。そのクレデンシャルで ``wss://<IoTデータエンドポイント>/mqtt`` のURLにSigV4署名を付け、MQTTで ``ui/<id>/state`` を購読する構成だった。デバイスがpublishした状態を画面へ数秒以内に反映したかった。

MQTTクライアントからは接続エラーが返り、IoTの接続ログには ``AUTHORIZATION_FAILURE`` が出ていた。最初はIoTポリシーかIAMの権限不足を疑ったが、403がどの通信で返ったかを先に確かめる必要があった。

WebSocketのHTTP upgradeと、その後に送るMQTT CONNECTは別の観測点になる。HTTP応答が403ならupgradeは成立していない。upgradeが成功しても、MQTT CONNECTやSUBSCRIBEの認可が通ったとは限らない。ログに ``AUTHORIZATION_FAILURE`` があるだけでは、その場のHTTP 403の原因を特定できなかった。


HTTP応答を直接見る
------------------

Node.jsの ``ws`` で、署名済みURLへのupgrade応答を確認した。下のコードは観測用の抜粋で、 ``signedUrl`` は別途生成したURLを渡す。

.. code-block:: javascript

   import WebSocket from 'ws';

   const ws = new WebSocket(signedUrl, ['mqtt'], { handshakeTimeout: 8000 });
   ws.on('open', () => console.log('UPGRADE OK'));
   ws.on('unexpected-response', (_request, response) => {
     let body = '';
     response.on('data', chunk => { body += chunk; });
     response.on('end', () => {
       console.log(response.statusCode, response.headers['x-amzn-errortype'], body);
     });
   });

この環境では ``403 ForbiddenException`` が返った。MQTTの認可を調べる前に、まずupgradeまでの条件を切り分ける。


署名までの切り分け
------------------

自前の署名処理だけに原因があるのかを確かめるため、当時使っていた ``@aws-sdk/signature-v4`` の ``presign()`` でもURLを作った。結果は同じ403。これで単純な自前の計算ミスという見立ては弱くなった。ただし、SDKで署名したからリクエスト全体が正しいとはまだ言えない。

WebSocketのsubprotocolを ``mqtt`` 、 ``mqttv3.1`` 、指定なしに変えても403は変わらなかった。同じ一時クレデンシャルを使ったHTTPSの ``iot-data publish`` は成功した。HTTPSのヘッダー署名では通り、WSSのクエリ署名では通らない。違いはそこまで絞れた。

IAMの ``iot:Connect`` 、 ``iot:Subscribe`` 、 ``iot:Receive`` はシミュレーター上で許可されていた。管理者クレデンシャルでもWSSの403が再現したため、少なくともIAM権限を追加するだけでは今回のHTTP 403を解消できない。検証中はIoTポリシーのクライアントID制約も一時的に緩めて試したが、結果は変わらなかった。検証後、この制約は元に戻している。


セッショントークンの位置
------------------------

`AWS IoT CoreのIAM認証の説明 <https://docs.aws.amazon.com/iot/latest/developerguide/iam-users-groups-roles.html>`_ を読み直すと、一般的なSigV4の説明だけでは見落とす条件があった。一時クレデンシャルでクエリ認証する場合、 ``X-Amz-Security-Token`` を署名対象のcanonical query stringに入れず、署名を計算した後でURLへ追加するというものだ。

自前の実装はトークンを署名対象に含めていた。当時の ``@aws-sdk/signature-v4`` の ``presign()`` も同様のURLを生成した。この挙動は `AWS SDK for JavaScript v3のissue #3417 <https://github.com/aws/aws-sdk-js-v3/issues/3417>`_ でも報告されている。SDKの挙動は版によって変わり得るので、採用中の版で生成されるcanonical queryを確認した方がよい。

修正時の順序は次のとおり。

#. ``X-Amz-Security-Token`` を除いたクエリでcanonical requestと署名を計算する。
#. ``X-Amz-Signature`` をURLへ付ける。
#. 一時クレデンシャルの ``X-Amz-Security-Token`` をURLエンコードして付ける。

この順序で作ったURLでは ``UPGRADE OK`` を確認できた。署名に関するHTTP 403はここで解消した。ただし、WebSocketが開いた段階では、まだ購読できるとは言えない。


MQTT側に残った認可エラー
--------------------------

upgradeを通した後はMQTT CONNECT側の認可を確認した。 ``aws iot list-targets-for-policy --policy-name <ポリシー名>`` の結果は空で、対象のCognito IdentityにIoTポリシーが付いていなかった。

`AWS IoT CoreのPublish/Subscribeポリシー例 <https://docs.aws.amazon.com/iot/latest/developerguide/pub-sub-policy.html>`_ によると、認証済みCognito IdentityでIoTの接続や購読などを行う場合、Identity PoolのIAMロールと、IdentityにアタッチしたIoTポリシーの両方で許可する必要がある。先ほど成功したHTTPS publishは、このMQTT over WebSocketの認可まで証明するものではなかった。

対象Identityへのアタッチを確認し、修正済みの署名URLで再接続した。今度はMQTT CONNECT、 ``ui/<id>/state`` のSUBSCRIBEが通り、別プロセスからpublishしたメッセージも受信した。最後に ``iot:Connect`` のリソースを ``client/${cognito-identity.amazonaws.com:sub}`` に戻し、clientIdにIdentity IDを指定して再確認した。検証のために広げた権限を残す必要はなかった。


アタッチ処理の配置
------------------

アプリへ組み込むなら、認証済みIdentityへのIoTポリシーのアタッチをどこで行うかも決める必要がある。`AWSのCognito Identity認可ガイド <https://docs.aws.amazon.com/iot/latest/developerguide/cog-iot-policies.html>`_ には、ブラウザ側で ``AttachPolicy`` を呼ぶ例と、Lambdaで代行する例がある。

ブラウザから直接呼ぶ方式では、利用者に管理APIの ``iot:AttachPolicy`` 権限を渡す。今回の構成なら、バックエンドで認証済みIdentity IDと許可対象を確認してから、決めたポリシーをアタッチする方針にしたい。実装する際は、アタッチ済みの場合の扱い、再ログイン時の確認、ポリシー変更時の反映も合わせて設計する。


今回の判断
----------

同じ403を見ていても、署名URLの修正とIoTポリシーのアタッチは別の作業だった。HTTP upgradeの応答を直接見ることで最初の失敗を切り出し、そこを通した後にMQTTの認可を確認できた。

画面のRESTポーリングが成功しているだけでは、リアルタイム購読が動いている証拠にはならない。次に同じ症状を見たら、HTTPのステータス、WebSocketのopen、MQTT CONNECT、SUBSCRIBE、実際の受信を順に確認する。
