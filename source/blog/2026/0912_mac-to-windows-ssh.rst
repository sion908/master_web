同一Wi-Fi上のMacからWindowsへSSH接続して公開鍵認証するまで
==========================================================

.. post:: 2026-09-12
   :tags: チュートリアル, ツール, 運用
   :author: sion908
   :language: ja
   :location: blog/2026

.. meta::
   :description:
     同一Wi-Fi上にあるMacからWindowsにSSH接続し、公開鍵認証でログインするまでの手順とトラブルシューティング。ネットワークプロファイル起因のタイムアウトや管理者アカウント特有のauthorized_keys配置など、詰まりやすいポイントをまとめました。


やりたかったことと全体の構成
----------------------------

同じWi-FiにMacとWindows PCが接続されている環境で、MacからWindowsをターミナル経由で操作できるようにしたかった。

目的は、Windows側でCodexやMCPなどを動かしつつ、手元の作業は使い慣れたMacから行いたいというもの。Tailscaleを導入する案も考えたが、まずは同じLAN内にいるため、シンプルなSSH接続で構成することにした。

最終的な構成は次の通り。

.. code-block:: text

   Mac
     │
     │ SSH（公開鍵認証 / briar.local）
     ▼
   Windows (briar)
     ├─ OpenSSH Server
     └─ Codex / MCPなどを実行

IPアドレスを固定せずともホスト名で接続でき、公開鍵認証でパスワード入力なしで入れる状態を目指した。


OpenSSH Serverのセットアップ
----------------------------

まずはWindows側でSSHサーバーが稼働しているか確認した。管理者権限のPowerShellを開いて実行する。

.. code-block:: powershell

   Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'

結果は ``State : NotPresent`` だった。SSH接続を受け付けるためのOpenSSH Serverがまだ入っていなかったため、そのままインストールした。

.. code-block:: powershell

   Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

インストール完了後、sshdサービスを起動し、PC再起動時にも自動で立ち上がるよう設定した。

.. code-block:: powershell

   Start-Service sshd
   Set-Service -Name sshd -StartupType Automatic

サービスの状態を確認する。

.. code-block:: powershell

   Get-Service sshd

``Status`` が ``Running`` になっていればサービス自体の立ち上げは完了。

続いてWindows Firewallの受信ルールを確認した。

.. code-block:: powershell

   Get-NetFirewallRule -Name *OpenSSH*

``OpenSSH-Server-In-TCP`` というルールが存在し、``Enabled : True``、``Action : Allow`` になっていた。

この時点では「サーバーも動いておりFirewallルールもあるので、すぐ繋がるだろう」と思っていた。しかし、ここで最初の壁にぶつかった。


接続タイムアウトとネットワークプロファイルの壁
----------------------------------------------

WindowsのIPアドレス（``ipconfig``）とユーザー名（``whoami``）を確認し、MacからSSH接続を試みた。

.. code-block:: bash

   ssh i3ci_@<WindowsのIPアドレス>

しかし、待たされた末にタイムアウトした。

.. code-block:: text

   Operation timed out

``ping`` も飛ばしてみたが、100%パケットロスで応答がない。Windowsは標準でICMP（ping）を遮断することが多いため、pingが通らないこと自体は決定打ではない。

Windows側でポートが空いているかを再確認した。

.. code-block:: powershell

   Get-NetTCPConnection -LocalPort 22 -State Listen

結果は ``0.0.0.0:22`` および ``[::]:22`` でしっかりとListenしていた。サーバー自体はポートを開いて待機している。

原因を調べるためネットワークプロファイルを確認した。

.. code-block:: powershell

   Get-NetConnectionProfile

出力を見ると、Wi-Fiのプロファイルが以下のようになっていた。

.. code-block:: text

   InterfaceAlias  : Wi-Fi
   NetworkCategory : Public

一方、先ほど確認したFirewallのルール ``OpenSSH-Server-In-TCP`` を見直すと、適用プロファイルが ``Private`` のみだった。

- 接続中のWi-Fi: Public
- OpenSSHの受信許可: Privateのみ

この食い違いにより、Firewallでパケットが落とされていた。自宅の管理下にあるWi-Fiなので、ネットワークカテゴリをPrivateに変更した。

.. code-block:: powershell

   Set-NetConnectionProfile -InterfaceAlias "Wi-Fi" -NetworkCategory Private

変更後、Macから再度SSHを実行すると、今度はタイムアウトせずにパスワードを要求される画面まで到達した。


ログインパスワードとホスト名解決
--------------------------------

SSH接続が進んだものの、パスワード入力で少し迷った。

普段Windowsへログインする際はWindows HelloのPINを使っている。しかし、SSHで要求されるパスワードはPINでは通らない。

Microsoftアカウントでサインインしている環境の場合、入力すべきなのはMicrosoftアカウント自体のパスワードだった。これを入力すると無事にログインできた。

また、DHCP環境ではWindowsのローカルIPが変わる可能性がある。ルーター側で固定IPを割り振ることも検討したが、MacからmDNS経由で名前解決できるか試してみた。

.. code-block:: bash

   ping briar.local

WindowsのPC名（ホスト名）に ``.local`` を付けたアドレス宛てにpingを打つと、正常に応答が返ってきた。

.. code-block:: bash

   ssh i3ci_@briar.local

この指定でそのまま繋がったため、ルーター設定やIP固定を行わず、ホスト名で接続することにした。


公開鍵認証と管理者ユーザーの落とし穴
------------------------------------

毎回Microsoftアカウントの長いパスワードを入力するのは手間なので、公開鍵認証を設定することにした。

Mac側でEd25519鍵を作成（または既存の鍵を確認）する。

.. code-block:: bash

   ssh-keygen -t ed25519
   cat ~/.ssh/id_ed25519.pub

Linux環境であれば ``~/.ssh/authorized_keys`` に追記すれば終わる話だが、WindowsのOpenSSHでは落とし穴がある。

対象のユーザーがAdministratorsグループに所属しているかを確認した。

.. code-block:: powershell

   net localgroup Administrators

普段使っているユーザー ``i3ci_`` がAdministratorsグループに含まれていた。

WindowsのOpenSSHのデフォルト設定（``sshd_config``）には、管理者グループ向けの特別な設定が入っている。

.. code-block:: text

   Match Group administrators
       AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys

ユーザーが管理者権限を持っている場合、ユーザーフォルダ下の ``~/.ssh/authorized_keys`` ではなく、システム共通の ``C:\ProgramData\ssh\administrators_authorized_keys`` が参照される。

そのため、公開鍵はこのファイルに配置する必要があった。


公開鍵の登録形式とACLの調整
----------------------------

Windows側の管理者権限PowerShellで、ファイルのアクセス権（ACL）を厳格に設定した。余計なアクセス権限が残っていると、OpenSSHがセキュリティ上の理由で鍵を拒否するためだ。

.. code-block:: powershell

   icacls "C:\ProgramData\ssh\administrators_authorized_keys" /inheritance:r
   icacls "C:\ProgramData\ssh\administrators_authorized_keys" /grant "Administrators:F"
   icacls "C:\ProgramData\ssh\administrators_authorized_keys" /grant "SYSTEM:F"
   Restart-Service sshd

これで鍵認証が通るはずだった。しかし、Macから詳細ログ付きで接続してみたところ、再びパスワード入力を求められた。

.. code-block:: bash

   ssh -v -i ~/.ssh/id_ed25519 i3ci_@briar.local

ログを確認すると、Mac側は公開鍵を提示しているものの、Windows側が受理せずパスワード認証へフォールバックしていた。

.. code-block:: text

   debug1: Offering public key: /Users/.../.ssh/id_ed25519 ED25519 ...
   debug1: Authentications that can continue: publickey,password,keyboard-interactive
   i3ci_@briar.local's password:

原因はファイルの書き込み方にあった。PowerShellからファイルを作成した際、公開鍵の文字列全体をダブルクォートで囲んでしまっていた。

.. code-block:: text

   # 誤っていた形式
   "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... mac-to-briar"

   # 正しい形式
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... mac-to-briar

余分な ``"`` が含まれていたため、OpenSSHが有効な公開鍵行として解釈できていなかった。ダブルクォートを取り除いてファイルを保存し直したところ、パスワードを聞かれることなく一瞬でログインできるようになった。


Mac側のSSH接続設定
------------------

接続が確認できたので、Mac側の ``~/.ssh/config`` に設定を追加した。

.. code-block:: text

   Host briar
       HostName briar.local
       User i3ci_
       IdentityFile ~/.ssh/id_ed25519
       IdentitiesOnly yes

これで、普段は短いコマンドだけで接続できる。

.. code-block:: bash

   ssh briar


その後：Tailscaleの導入
-----------------------

同一Wi-FiでのSSH接続が安定したあと、気になっていたTailscaleも導入してみた。

こちらも拍子抜けするほど簡単だった。MacとWindowsの両方にTailscaleをインストールしてサインインするだけで、特別なルーティング設定なしにあっさり疎通できた。

変わったことといえば名前解決くらい。MagicDNSが有効になるため、接続先のホスト名がローカルの ``briar.local`` から ``briar.tailscaleXXXX.ts.net`` のようなTailscaleドメインに変わった。

Mac側の ``~/.ssh/config`` を書き換える。

.. code-block:: text

   Host briar
       HostName briar.tailscaleXXXX.ts.net
       User i3ci_
       IdentityFile ~/.ssh/id_ed25519
       IdentitiesOnly yes

Windows側のOpenSSHや公開鍵の配置はそのまま流用できる。これだけで、Wi-Fiの接続先が変わっても同じ ``ssh briar`` で繋がるようになった。


振り返りとまとめ
----------------

同一Wi-Fi内であればローカルSSHとmDNS（``.local``）だけでも十分実用的だったし、Tailscaleを重ねればネットワーク環境の制約すらなくなった。どちらを選ぶにしても、Windows側のSSH設定が土台になる。

今回引っかかったポイントは主に3点。

1. **Firewallとネットワークプロファイルの不一致**: sshdが起動していても、Wi-FiがPublicカテゴリになっていると受信パケットが遮断される。
2. **ログイン認証の仕様**: Windows HelloのPINではなく、Microsoftアカウントのパスワードが求められる。
3. **管理者ユーザーのauthorized_keys**: Administratorsグループ所属のアカウントは配置場所が異なり、ファイルパーミッション（icacls）や鍵の記述形式にも注意を払う必要がある。

Macからホスト名指定ひとつでWindows環境へ潜れるようになったことで、マシンごとの役割分担がかなりスムーズになった。
