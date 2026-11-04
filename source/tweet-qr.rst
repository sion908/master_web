X (Twitter) 投稿用QRコード作成ツール
====================================

.. meta::
   :description: イベントや勉強会、登壇スライド向けのX(Twitter)投稿用QRコードを即座に作成・ダウンロードできるツール。ハッシュタグや本文を設定して共有用QRコードを生成できます。

.. raw:: html

   <div class="qr-tool-container">
       <div class="qr-hero">
           <span class="badge"><i class="fas fa-qrcode"></i> 便利ツール</span>
           <h1>イベント用 X (Twitter) 投稿QRコード作成</h1>
           <p class="lead">
               勉強会やカンファレンスの登壇スライド、会場掲示に便利なX(Twitter)投稿用QRコードジェネレーターです。<br>
               ハッシュタグや本文を指定すると、読み取るだけで投稿画面が開くQRコードを即座に作成・ダウンロードできます。
           </p>
       </div>

       <div class="qr-grid">
           <!-- 左カラム: 設定フォーム -->
           <div class="qr-card config-card">
               <h2><i class="fas fa-sliders-h"></i> 投稿内容の設定</h2>

               <div class="form-group">
                   <label for="tweet-text">
                       <strong>本文</strong>
                       <span class="help-text">投稿画面の初期テキスト（デフォルト: わいわい）</span>
                   </label>
                   <textarea id="tweet-text" rows="3" placeholder="わいわい">わいわい</textarea>
               </div>

               <div class="form-group">
                   <label for="tweet-tags">
                       <strong>ハッシュタグ</strong>
                       <span class="help-text">カンマまたはスペース区切り（# は不要です）</span>
                   </label>
                   <input type="text" id="tweet-tags" placeholder="jawsug, jawsug_nagasaki" value="jawsug">
               </div>

               <div class="form-group">
                   <label for="tweet-url">
                       <strong>添付URL（任意）</strong>
                       <span class="help-text">イベントページやスライドのURL</span>
                   </label>
                   <input type="url" id="tweet-url" placeholder="https://connpass.com/event/...">
               </div>

               <div class="form-group">
                   <label for="qr-size">
                       <strong>QRコード画像サイズ</strong>
                       <span class="help-text">スライドや印刷物用には大きめがおすすめです</span>
                   </label>
                   <select id="qr-size">
                       <option value="256">標準 (256 x 256 px)</option>
                       <option value="512" selected>高解像度 (512 x 512 px) - スライド推奨</option>
                       <option value="1024">特大 (1024 x 1024 px) - 印刷推奨</option>
                   </select>
               </div>
           </div>

           <!-- 右カラム: プレビュー & 出力 -->
           <div class="qr-card preview-card">
               <h2><i class="fas fa-eye"></i> QRコードプレビュー</h2>

               <div class="qr-display-wrapper">
                   <div id="qrcode-display" class="qrcode-box"></div>
                   <p class="qr-caption">スマートフォンのカメラで読み取ってテストできます</p>
               </div>

               <div class="qr-actions">
                   <button id="download-btn" class="btn btn-primary btn-block" type="button">
                       <i class="fas fa-download"></i> QRコード画像を保存 (PNG)
                   </button>
                   <a id="test-tweet-btn" class="btn btn-outline btn-block" href="#" target="_blank" rel="noopener">
                       <i class="fab fa-twitter"></i> X(Twitter)で投稿を試す
                   </a>
               </div>

               <div class="form-group url-group">
                   <label for="generated-url"><strong>生成された投稿用URL</strong></label>
                   <div class="url-input-wrap">
                       <input type="text" id="generated-url" readonly>
                       <button id="copy-btn" class="btn btn-copy" type="button" title="URLをコピー">
                           <i class="fas fa-copy"></i>
                       </button>
                   </div>
               </div>
           </div>
       </div>

       <!-- 下部: スライド掲載のコツ -->
       <div class="qr-card tips-card">
           <h2><i class="fas fa-lightbulb"></i> スライド・会場で使うときのTips</h2>
           <div class="tips-grid">
               <div class="tip-item">
                   <h4><i class="fas fa-expand-alt"></i> 白い余白を残す</h4>
                   <p>QRコードの周囲には一定の白い余白（クワイエットゾーン）が必要です。背景と同化させず、白背景の四角枠ごとスライドに貼り付けると読み取りやすくなります。</p>
               </div>
               <div class="tip-item">
                   <h4><i class="fas fa-compress-arrows-alt"></i> 本文は簡潔に</h4>
                   <p>本文やURLが長くなりすぎると、QRコードのドットが細かくなり、プロジェクターの解像度や遠くの座席から読み取りにくくなります。短い本文がベストです。</p>
               </div>
               <div class="tip-item">
                   <h4><i class="fas fa-mobile-alt"></i> 会場からテスト確認</h4>
                   <p>スライド投影時、会場の後方席や左右の端からスマホカメラを向けて実際に読み取れるか、リハーサル時に確認しておくと安心です。</p>
               </div>
           </div>
       </div>
   </div>

   <!-- QRCode.js (CDN) -->
   <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>

   <style>
   .qr-tool-container {
       max-width: 1000px;
       margin: 0 auto;
       padding: 1rem 0 3rem;
   }
   .qr-hero {
       margin-bottom: 2rem;
       text-align: center;
   }
   .qr-hero .badge {
       display: inline-block;
       background: rgba(43, 114, 186, 0.12);
       color: #2b72ba;
       padding: 0.35rem 0.85rem;
       border-radius: 999px;
       font-size: 0.85rem;
       font-weight: 600;
       margin-bottom: 0.75rem;
   }
   html[data-theme="dark"] .qr-hero .badge {
       background: rgba(84, 160, 255, 0.2);
       color: #70a1ff;
   }
   .qr-hero h1 {
       font-size: 2rem;
       margin-bottom: 0.75rem;
       line-height: 1.3;
   }
   .qr-hero .lead {
       font-size: 1rem;
       opacity: 0.85;
       max-width: 720px;
       margin: 0 auto;
       line-height: 1.6;
   }

   .qr-grid {
       display: grid;
       grid-template-columns: 1fr 1fr;
       gap: 1.5rem;
       margin-bottom: 2rem;
   }
   @media (max-width: 768px) {
       .qr-grid {
           grid-template-columns: 1fr;
       }
   }

   .qr-card {
       background: var(--card-bg, #ffffff);
       border: 1px solid var(--border-color, #e2e8f0);
       border-radius: 12px;
       padding: 1.5rem;
       box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
   }
   html[data-theme="dark"] .qr-card {
       background: #1e293b;
       border-color: #334155;
       box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
   }
   .qr-card h2 {
       font-size: 1.25rem;
       margin-top: 0;
       margin-bottom: 1.25rem;
       display: flex;
       align-items: center;
       gap: 0.5rem;
       border-bottom: 2px solid var(--border-color, #f1f5f9);
       padding-bottom: 0.75rem;
   }
   html[data-theme="dark"] .qr-card h2 {
       border-bottom-color: #334155;
   }

   .form-group {
       margin-bottom: 1.25rem;
   }
   .form-group label {
       display: block;
       margin-bottom: 0.4rem;
   }
   .form-group label strong {
       display: inline-block;
       font-size: 0.95rem;
   }
   .form-group .help-text {
       display: block;
       font-size: 0.8rem;
       opacity: 0.7;
       margin-top: 0.15rem;
   }
   .form-group input[type="text"],
   .form-group input[type="url"],
   .form-group select,
   .form-group textarea {
       width: 100%;
       box-sizing: border-box;
       padding: 0.65rem 0.85rem;
       border: 1px solid var(--border-color, #cbd5e1);
       border-radius: 8px;
       font-size: 0.95rem;
       font-family: inherit;
       background: var(--bg-color, #ffffff);
       color: var(--text-color, #0f172a);
       transition: border-color 0.2s, box-shadow 0.2s;
   }
   html[data-theme="dark"] .form-group input[type="text"],
   html[data-theme="dark"] .form-group input[type="url"],
   html[data-theme="dark"] .form-group select,
   html[data-theme="dark"] .form-group textarea {
       background: #0f172a;
       border-color: #475569;
       color: #f1f5f9;
   }
   .form-group input:focus,
   .form-group select:focus,
   .form-group textarea:focus {
       outline: none;
       border-color: #2b72ba;
       box-shadow: 0 0 0 3px rgba(43, 114, 186, 0.2);
   }

   /* QRコード表示枠 */
   .qr-display-wrapper {
       text-align: center;
       margin-bottom: 1.25rem;
   }
   .qrcode-box {
       display: inline-flex;
       justify-content: center;
       align-items: center;
       background: #ffffff !important;
       padding: 16px;
       border-radius: 12px;
       box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
       max-width: 100%;
   }
   .qrcode-box img,
   .qrcode-box canvas {
       max-width: 240px;
       max-height: 240px;
       width: auto !important;
       height: auto !important;
       display: block;
   }
   .qr-caption {
       font-size: 0.8rem;
       opacity: 0.7;
       margin-top: 0.5rem;
   }

   .qr-actions {
       display: flex;
       flex-direction: column;
       gap: 0.65rem;
       margin-bottom: 1.25rem;
   }
   .btn-block {
       display: flex;
       align-items: center;
       justify-content: center;
       gap: 0.5rem;
       width: 100%;
       box-sizing: border-box;
       padding: 0.75rem 1rem;
       font-size: 0.95rem;
       font-weight: 600;
       border-radius: 8px;
       text-decoration: none;
       cursor: pointer;
   }

   .url-input-wrap {
       display: flex;
       gap: 0.5rem;
   }
   .url-input-wrap input {
       flex: 1;
       font-family: 'JetBrains Mono', monospace;
       font-size: 0.85rem;
   }
   .btn-copy {
       background: var(--border-color, #e2e8f0);
       color: var(--text-color, #0f172a);
       border: none;
       padding: 0 1rem;
       border-radius: 8px;
       cursor: pointer;
       font-size: 1rem;
       transition: background 0.2s;
   }
   html[data-theme="dark"] .btn-copy {
       background: #334155;
       color: #f1f5f9;
   }
   .btn-copy:hover {
       opacity: 0.85;
   }

   /* Tips */
   .tips-grid {
       display: grid;
       grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
       gap: 1.25rem;
   }
   .tip-item h4 {
       font-size: 1rem;
       margin-top: 0;
       margin-bottom: 0.4rem;
       display: flex;
       align-items: center;
       gap: 0.4rem;
       color: #2b72ba;
   }
   html[data-theme="dark"] .tip-item h4 {
       color: #70a1ff;
   }
   .tip-item p {
       font-size: 0.85rem;
       line-height: 1.6;
       opacity: 0.85;
       margin: 0;
   }
   </style>

   <script>
   document.addEventListener('DOMContentLoaded', function() {
       const textInput = document.getElementById('tweet-text');
       const tagsInput = document.getElementById('tweet-tags');
       const urlInput = document.getElementById('tweet-url');
       const sizeSelect = document.getElementById('qr-size');
       const qrContainer = document.getElementById('qrcode-display');
       const generatedUrlInput = document.getElementById('generated-url');
       const testTweetBtn = document.getElementById('test-tweet-btn');
       const downloadBtn = document.getElementById('download-btn');
       const copyBtn = document.getElementById('copy-btn');

       let qrcodeInstance = null;

       function buildTweetUrl() {
           const baseUrl = 'https://twitter.com/intent/tweet';
           const params = new URLSearchParams();

           const text = textInput.value.trim();
           if (text) {
               params.set('text', text);
           }

           const rawTags = tagsInput.value.trim();
           if (rawTags) {
               const tags = rawTags
                   .split(/[\s,、]+/)
                   .map(t => t.trim().replace(/^#+/, ''))
                   .filter(t => t.length > 0);
               if (tags.length > 0) {
                   params.set('hashtags', tags.join(','));
               }
           }

           const url = urlInput.value.trim();
           if (url) {
               params.set('url', url);
           }

           const query = params.toString();
           return query ? `${baseUrl}?${query}` : baseUrl;
       }

       function renderQR() {
           const tweetUrl = buildTweetUrl();
           const size = parseInt(sizeSelect.value, 10) || 512;

           generatedUrlInput.value = tweetUrl;
           testTweetBtn.href = tweetUrl;

           qrContainer.innerHTML = '';
           qrcodeInstance = new QRCode(qrContainer, {
               text: tweetUrl,
               width: size,
               height: size,
               colorDark: "#000000",
               colorLight: "#ffffff",
               correctLevel: QRCode.CorrectLevel.M
           });
       }

       // イベントリスナー設定
       textInput.addEventListener('input', renderQR);
       tagsInput.addEventListener('input', renderQR);
       urlInput.addEventListener('input', renderQR);
       sizeSelect.addEventListener('change', renderQR);

       // ダウンロード機能
       downloadBtn.addEventListener('click', function() {
           const canvas = qrContainer.querySelector('canvas');
           let dataUrl = '';
           if (canvas) {
               dataUrl = canvas.toDataURL('image/png');
           } else {
               const img = qrContainer.querySelector('img');
               if (img) dataUrl = img.src;
           }

           if (dataUrl) {
               const a = document.createElement('a');
               a.href = dataUrl;
               a.download = 'x-post-qr.png';
               document.body.appendChild(a);
               a.click();
               document.body.removeChild(a);
           }
       });

       // コピー機能
       copyBtn.addEventListener('click', function() {
           navigator.clipboard.writeText(generatedUrlInput.value).then(function() {
               const origHtml = copyBtn.innerHTML;
               copyBtn.innerHTML = '<i class="fas fa-check" style="color: #10b981;"></i>';
               setTimeout(function() {
                   copyBtn.innerHTML = origHtml;
               }, 2000);
           });
       });

       // 初期レンダリング
       renderQR();
   });
   </script>
