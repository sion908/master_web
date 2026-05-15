AIペアプログラミングで体感する未来の開発：Lambda + HTMX で30分ゲーム開発の全記録
==========================================================================================

.. post:: 2025-06-29
   :tags: HTMX, AmazonQ, AI, Lambda
   :author: sion908
   :language: ja
   :location: blog/2025

.. meta::
   :description: AmazonQ DeveloperのAIペアプログラミング機能を使って、HTMX+Lambdaでタイミングベースクリッカーゲームを30分で開発した全記録。

はじめに：開発革命の実体験
--------------------------

衝撃の30分間
^^^^^^^^^^^^^^^^

「AWSでゲームを作りたい」と入力してから、完全に動作するタイミングベースクリッカーゲームが完成するまで、わずか30分。これは誇張ではなく、実際に体験した開発速度です。

従来開発との比較
^^^^^^^^^^^^^^^^^^^^^^

従来の個人開発:
企画(1日) → 技術調査(2日) → 環境構築(半日) → 実装(1週間) → デバッグ(2日) → デプロイ(半日)
合計: 約2週間

AI支援開発:
企画・実装・デプロイ: 30分

この圧倒的な差は何から生まれるのか？実際の開発プロセスを詳細に記録しました。

AI支援開発の実際：対話ログから見る開発プロセス
----------------------------------------------

Phase 1: 技術スタック選定（5分）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**私**: 「awsに置くことを念頭に置いたゲームを作りたい」

**AI**: 即座に複数の選択肢を提示
- Webブラウザゲーム（S3 + CloudFront + Lambda）
- リアルタイム対戦（GameLift + WebSocket）
- モバイルゲーム（Amplify + Cognito）

**私**: 「lambda+jinja2+htmxである」

**AI**: 瞬時に最適化された構成を提案

Lambda Function URLs + Jinja2 + HTMX
↓
サーバーレス + テンプレート + ハイパーメディア
= 最小構成で最大効果

Phase 2: 基本実装（10分）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

AIが生成した初期コードの品質に驚愕：
- Litestarの適切な使用法
- Jinja2テンプレートのインライン実装
- HTMXの効果的な活用
- エラーハンドリングまで完備

Phase 3: 機能拡張（10分）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**私**: 「litestarも使って欲しい」
→ 即座にMangumを使ったLambda統合

**私**: 「localStorageに保存するようにして欲しい」
→ クライアント・サーバー間の状態同期システムを実装

Phase 4: UX改善（5分）
^^^^^^^^^^^^^^^^^^^^^^^^^^

**私**: 「htmxの機能を何か使いたい」
→ プログレスバー、アニメーション、リアルタイム更新を提案・実装

Lambda + HTMX: 新時代のWeb開発パラダイム
------------------------------------------

従来のSPA開発の課題
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: javascript

   // React/Vueの典型的な複雑さ
   const [gameState, setGameState] = useState({});
   const [loading, setLoading] = useState(false);

   useEffect(() => {
    // 複雑な状態管理
    // API呼び出し
    // エラーハンドリング
   }, [dependencies]);

   // ビルド設定、バンドル最適化、デプロイ設定...

HTMX + Lambdaのシンプルさ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: html

   <!-- たった1行でリアルタイム更新 -->
   <button hx-post="/api/action" 
          hx-target="#game-content">
      Click Me!
   </button>

技術的優位性の詳細分析
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. 開発効率

   - **フロントエンド・バックエンド境界の消失**
   - HTMLテンプレート内でサーバーロジックを直接呼び出し
   - 状態管理の複雑さを排除
   - APIの設計・実装コストを削減

2. 想定運用コスト

   従来構成の月額コスト:

   - EC2 t3.micro: $8.5
   - RDS t3.micro: $15
   - CloudFront: $1
   - 合計: $24.5/月

   Lambda + HTMX構成:

   - Lambda実行時間: $0.20
   - API Gateway: $1
   - 合計: $1.20/月 (95%削減)

3. パフォーマンス

   - **初期ロード**: HTMLテンプレート直接配信
   - **更新処理**: 必要な部分のみDOM更新
   - **ネットワーク**: JSONではなくHTML断片で通信効率化

実装の技術的深掘り
--------------------

HTMXの真の威力
^^^^^^^^^^^^^^^^^^^^^^^^

1. 宣言的UI更新
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: html

   <!-- 従来のJavaScript -->
   <script>
   fetch('/api/action', {method: 'POST'})
    .then(response => response.json())
    .then(data => {
      document.getElementById('score').textContent = data.score;
      document.getElementById('level').textContent = data.level;
      // 複雑なDOM操作...
    });
   </script>

   <!-- HTMXの宣言的アプローチ -->
   <button hx-post="/api/action" 
          hx-target="#game-content"
          hx-swap="innerHTML">
      Click Me!
   </button>

2. 高度な機能の簡単実装
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: html

   <!-- プログレスインジケーター -->
   <div hx-indicator="#loading">Processing...</div>

   <!-- 条件付きリクエスト -->
   <div hx-get="/api/special" 
       hx-trigger="load"
       hx-include="[name='level']">
   </div>

   <!-- リアルタイム更新 -->
   <div hx-get="/api/status" 
       hx-trigger="every 2s">
   </div>

Lambdaでのゲーム状態管理
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. localStorageとの連携パターン
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def get_game_data_from_request(request: Request) -> Dict[str, int]:
      """HTTPヘッダーからクライアント状態を取得"""
      game_data_header = request.headers.get('X-Game-Data')
      if game_data_header:
          return json.loads(game_data_header)
      return {'score': 0, 'clicks': 0, 'level': 1}

   def create_response_with_game_data(template_name: str, game_data: Dict[str, int], context):
      """更新された状態をヘッダーで返却"""
      headers = {'X-Updated-Game-Data': json.dumps(game_data)}
      return LitestarResponse(content=html, headers=headers)

2. タイミングシステムの実装
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: javascript

   function attemptItemGet(event) {
      // リアルタイム位置計算
      const position = calculateIndicatorPosition(event);
      
      // タイミング品質判定
      const quality = determineTimingQuality(position);
      
      // HTMXでサーバーに送信
      htmx.ajax('POST', '/api/get-item', {
          headers: {'X-Timing-Quality': quality}
      });
   }

AI支援開発の深層分析
----------------------

AIが優秀だった点
^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. 技術選択の最適化
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **問題**: 「AWSでゲーム」という曖昧な要求
- **AI判断**: 用途に応じた複数選択肢の提示
- **結果**: 最小構成で最大効果の実現

2. 実装パターンの知識
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

AIが自然に適用したベストプラクティス:

- Mangumを使ったLambda統合
- Jinja2のStringLoaderパターン
- HTMXイベントハンドリング
- エラーハンドリングの網羅

3. デバッグ能力
^^^^^^^^^^^^^^^^^

エラー: ImportError: cannot import name 'FormData'
AI対応: 即座に不要なインポートを特定・削除

エラー: AttributeError: 'StringTemplateEngine' object has no attribute 'engine'
AI対応: テンプレートエンジンの実装方式を変更

人間が重要だった点
^^^^^^^^^^^^^^^^^^^^^^^^^^

1. 要求の具体化
^^^^^^^^^^^^^^^^^^^^^
- 「プログレスバーを表示し、特定の場所をクリックするとアイテムがもらえるように」
- 「スコアはlocalStorageに保存するようにして欲しい」

2. UX判断
^^^^^^^^^^
- タイミングゲームの面白さ
- 視覚効果の豪華さ
- ユーザビリティの向上

3. 技術選択の最終判断
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Lambda + HTMXの組み合わせ採用
- localStorageでの永続化選択

開発体験の革新
----------------

従来の個人開発
^^^^^^^^^^^^^^^^^^^^　

1. アイデア発想
2. 技術調査・学習
3. 環境構築
4. 設計・実装
5. テスト・デバッグ
6. デプロイ設定
7. 運用準備

各段階で挫折リスク

AI支援開発
^^^^^^^^^^^^^^^^^^

1. アイデア発想
2. AIとの対話で即座に実装
3. リアルタイムでの改善・拡張

挫折リスクの大幅削減

学習効果の変化
^^^^^^^^^^^^^^^^^^^^^^
- **従来**: 理論学習 → 実践適用
- **AI支援**: 実践 → 理解深化
- **結果**: より深い技術理解

まとめ：開発パラダイムの転換点
------------------------------

AI支援開発の本質
^^^^^^^^^^^^^^^^^^^^^^^^^
- **速度**: アイデア→実装の時間短縮
- **品質**: ベストプラクティスの自動適用
- **学習**: 実践を通じた深い理解

Lambda + HTMX の意義
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **シンプルさ**: 複雑さを排除した開発体験
- **効率性**: 最小コストでの最大効果
- **拡張性**: 必要に応じた機能追加の容易さ

個人開発者への提言
^^^^^^^^^^^^^^^^^^^^^^^^^^
1. **AIを恐れず活用**: 協働パートナーとしての位置づけ
2. **技術選択の再考**: 複雑さより実用性を重視
3. **学習方法の変化**: 理論より実践を先行

最後に
^^^^^^^^

この30分間の開発体験は、単なる技術的成功以上の意味を持ちます。それは、個人開発者が世界レベルの開発速度と品質を手に入れられる時代の到来を示しています。

技術の民主化が進む今、重要なのは最新フレームワークの習得ではなく、**問題解決能力**と**創造性**です。AIが技術的な実装を支援してくれる今こそ、私たちは本来注力すべき「何を作るか」「なぜ作るか」に集中できるのです。

参考リンク・リソース
--------------------

- `HTMX公式ドキュメント <https://htmx.org/>`_
- `Litestar公式ドキュメント <https://litestar.dev/>`_
- `AWS SAM公式ガイド <https://docs.aws.amazon.com/serverless-application-model/>`_

---

*この記事は実際のAI支援開発体験を基に執筆されました。開発時間30分は実測値です。*
