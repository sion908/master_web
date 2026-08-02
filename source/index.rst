Python、Web開発、クラウド技術
==============================

.. raw:: html

   <div class="portal-container">

       <!-- 3カラムポータルグリッド (PCで 左: About Me | 中央: Welcome + 最新記事 | 右: Services) -->
       <div class="portal-grid">

           <!-- 左カラム: About Me -->
           <aside class="portal-sidebar-left">
               <section class="premium-card profile-section">
                   <div class="card-content">
                       <div class="profile-header">
                           <i class="fas fa-user-circle"></i>
                           <h3>About Me</h3>
                       </div>
                       <p>長崎を拠点に活動するバックエンドエンジニアです。<br>AWSサーバレス構成を中心としたWebアプリケーションの開発・運用を本業としつつ、個人でもWebサービスの企画・開発・運営や地域コミュニティの技術支援に取り組んでいます。</p>
                       <ul class="profile-skills">
                           <li><i class="fas fa-code"></i> Python / AWS / TypeScript</li>
                           <li><i class="fas fa-server"></i> サーバレス / Lambda / Docker</li>
                           <li><i class="fas fa-users"></i> JAWS-UG長崎 運営</li>
                       </ul>
                       <a href="https://portfolio.sion908.tech/" class="btn btn-outline">
                           <i class="fas fa-external-link-alt"></i>
                           実績・経歴（ポートフォリオ）を見る
                       </a>
                   </div>
               </section>
           </aside>

           <!-- 中央メイン: Welcome + 最新記事 -->
           <main class="portal-main">

               <!-- 1. Hero Section (挨拶) -->
               <section class="premium-card hero-section">
                   <div class="card-content">
                       <div class="hero-header">
                           <span class="hero-badge"><i class="fas fa-sparkles"></i> Welcome to sion908 lab</span>
                           <h2 class="hero-title">Sion908 lab Blog</h2>
                           <p class="hero-tagline">長崎から発信する、Python・Web開発・クラウド技術の技術メモ＆ブログ</p>
                       </div>
                       <p class="hero-description">
                           このサイトは、長崎を拠点に活動するバックエンドエンジニア <strong>sion908</strong> の個人ポータル兼技術ブログです。日々学んだことや、AWSサーバーレス構成、Python、TypeScriptでの開発ノウハウ、地域コミュニティ（JAWS-UG長崎など）の活動報告などを発信しています。
                       </p>
                   </div>
               </section>

               <!-- 2. Latest Posts (最新記事) -->
               <section class="premium-card latest-posts">
                   <div class="card-content">
                       <h3>最新記事</h3>
                       <p class="section-subtitle">技術トレンドから実践的なノウハウまで</p>

.. postlist:: 10
   :date: %Y-%m-%d
   :format: {date} {title}
   :list-style: none
   :tags:
   :excerpts:

.. raw:: html

                       <div class="cta-section">
                           <a href="blog.html" class="btn btn-primary">
                               <i class="fas fa-arrow-right"></i>
                               すべての記事を見る
                           </a>
                           <a href="tags.html" class="btn btn-outline">
                               <i class="fas fa-tags"></i>
                               タグクラウドで探す
                           </a>
                       </div>
                   </div>
               </section>
           </main>

           <!-- 右カラム: Supported Services -->
           <aside class="portal-sidebar-right">
               <section class="premium-card services-section">
                   <div class="card-content">
                       <h3>Supported Services</h3>
                       <div class="services-grid">
                           <div class="service-item">
                               <i class="fas fa-book"></i>
                               <h4>まめここ</h4>
                               <p>GTFSデータの可視化・管理プラットフォーム</p>
                               <a href="https://www.mamekoko.sion908.tech/">Go to Site</a>
                           </div>
                           <div class="service-item">
                               <i class="fas fa-presentation"></i>
                               <h4>スライド</h4>
                               <p>登壇資料や技術解説スライドのアーカイブ</p>
                               <a href="https://slide.sion908.tech/">Browse Slides</a>
                           </div>
                           <div class="service-item">
                               <i class="fas fa-calendar-alt"></i>
                               <h4>長崎ITイベントカレンダー</h4>
                               <p>長崎県内の技術イベントを集約した公開カレンダー</p>
                               <a href="nagasaki-tech-calendar.html">View Calendar</a>
                           </div>
                       </div>
                   </div>
               </section>
           </aside>

       </div>

   </div>

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   blog
   tags
   nagasaki-tech-calendar
   contact
   privacy
