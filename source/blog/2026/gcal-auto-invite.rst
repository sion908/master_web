Googleカレンダーの招待を自動化したら地味に人生が楽になった話
==============================================================

.. post:: 2026-03-28
   :tags: GAS, Google Calendar, 自動化, 個人開発, ライフハック
   :author: sion908
   :language: ja
   :location: blog/2026

はじめに
--------

奥さんとの予定をGoogleカレンダーで共有することにした。

ただ、予定を入れるときに共有を忘れることが多い。後から「あ、共有してなかった」と気づいて、慌てて招待する。これの繰り返し。

「自動化しなければ」と思い立って、GASで毎日4時に自動で奥さんを招待する仕組みを作った。派手な機能じゃないけど、日常のストレスは確実に減った。

何を作ったか
-----------

毎日4時に以下の処理を自動実行：

- 今日以降の予定をチェック
- 自分が作った予定だけを対象
- タイトル末尾に ``[skip]`` がついていない予定に限定
- 指定したメールアドレスをゲストとして追加

実装のポイント
--------------

### 1. isOwnedByMe() で自分の予定だけを対象

招待された予定には自動で招待を追加しない。これが重要。

.. code-block:: javascript

   if (!event.isOwnedByMe()) {
     continue;
   }

### 2. [skip] で制御

タイトルに ``[skip]`` をつけるだけで除外。シンプルな運用ルール。

.. code-block:: javascript

   if (title.endsWith(skipSuffix)) {
     continue;
   }

### 3. 既に招待済みならスキップ

同じ人を何度も招待しない。

.. code-block:: javascript

   const guestList = event.getGuestList().map(g => g.getEmail().toLowerCase());
   if (guestList.includes(guestEmail.toLowerCase())) {
     continue;
   }

実装全体
--------

TypeScriptで書いて、claspでローカル管理。

.. code-block:: typescript

   function setConfig(): void {
     const props = PropertiesService.getScriptProperties();
     props.setProperties({
       TARGET_GUEST_EMAIL: "info@sample.com",
       CALENDAR_ID: "primary",
       SKIP_SUFFIX: "[skip]"
     });
   }

   function inviteGuestToUpcomingEvents(): void {
     const props = PropertiesService.getScriptProperties();
     const guestEmail = props.getProperty("TARGET_GUEST_EMAIL");
     const calendarId = props.getProperty("CALENDAR_ID") || "primary";
     const skipSuffix = props.getProperty("SKIP_SUFFIX") || "[skip]";

     if (!guestEmail) {
       throw new Error("TARGET_GUEST_EMAIL が未設定です。setConfig() を実行してください。");
     }

     const calendar =
       calendarId === "primary"
         ? CalendarApp.getDefaultCalendar()
         : CalendarApp.getCalendarById(calendarId);

     if (!calendar) {
       throw new Error(`カレンダーが見つかりません: ${calendarId}`);
     }

     const now = new Date();
     const oneYearLater = new Date(now);
     oneYearLater.setFullYear(oneYearLater.getFullYear() + 1);

     const events = calendar.getEvents(now, oneYearLater);

     for (const event of events) {
       const title = (event.getTitle() || "").trim();

       if (title.endsWith(skipSuffix) || !event.isOwnedByMe()) {
         continue;
       }

       const guestList = event.getGuestList().map(g => g.getEmail().toLowerCase());
       if (guestList.includes(guestEmail.toLowerCase())) {
         continue;
       }

       try {
         event.addGuest(guestEmail);
         console.log(`追加: ${title} -> ${guestEmail}`);
       } catch (e) {
         console.error(`追加失敗: ${title} / ${e}`);
       }
     }
   }

   function createDailyTrigger(): void {
     const functionName = "inviteGuestToUpcomingEvents";

     const triggers = ScriptApp.getProjectTriggers();
     for (const trigger of triggers) {
       if (trigger.getHandlerFunction() === functionName) {
         console.log("既存トリガーあり");
         return;
       }
     }

     ScriptApp.newTrigger(functionName)
       .timeBased()
       .everyDays(1)
       .atHour(4)
       .create();

     console.log("毎日4時のトリガーを作成しました");
   }

   function updateGuestEmail(newEmail: string): void {
     PropertiesService.getScriptProperties().setProperty("TARGET_GUEST_EMAIL", newEmail);
   }

セットアップ手順
----------------

### 1. clasp をインストール

.. code-block:: bash

   npm install -g @google/clasp

### 2. ログイン

.. code-block:: bash

   clasp login

### 3. 既存GASをpull（またはclone）

スクリプトIDはURLから取得：

.. code-block:: bash

   clasp clone <SCRIPT_ID>

### 4. 初期設定を実行

Google Apps Script エディタで以下を実行：

.. code-block:: javascript

   setConfig()

### 5. トリガーを作成

.. code-block:: javascript

   createDailyTrigger()

失敗談
------

最初は全予定に招待を飛ばしていて、招待されたミーティングにも勝手に人が追加されるという事故が発生。

``isOwnedByMe()`` チェックを入れてからは安定した。

運用ルール
----------

- タイトル末尾に ``[skip]`` をつけると除外される (家賃の支払い予定など)
- 自分が作った予定だけが対象
- 既に招待済みなら何もしない
- メールアドレスは ``updateGuestEmail()`` で変更可能

ちょっとした工夫で生活が楽になる
---------------------------------

こういう「ちょっとした面倒」を仕組みで消していくのは結構好きで、派手な機能じゃないけど、日常のストレスは確実に減る。

こういうのを積み上げると、生活の解像度が少し上がる気がする。

次のステップ
-----------

- Slackへの通知追加
- 複数メールアドレスへの対応
- カレンダーごとの設定分岐

参考リンク
----------

- `Google Calendar Auto Invite GitHub <https://github.com/sion908/gcal-auto-invite>`_
- `Google Apps Script Documentation <https://developers.google.com/apps-script>`_
- `clasp GitHub <https://github.com/google/clasp>`_
- `Google Calendar API <https://developers.google.com/calendar>`_
