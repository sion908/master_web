from docutils.parsers.rst import Directive, directives
from docutils.nodes import raw


class TwitterDirective(Directive):
    """Twitter埋め込み用のカスタムディレクティブ"""

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False

    option_spec = {
        'theme': directives.unchanged,
    }

    def run(self):
        tweet_id = self.arguments[0]

        # オプションで指定されたテーマを優先、なければドキュメントのメタデータから取得
        theme = self.options.get('theme')
        if not theme:
            # ドキュメントのメタデータから twitter_theme を取得
            doc = self.state.document
            theme = doc.get('twitter_theme', 'light')

        # Twitter埋め込みコードを生成
        html = f'''<blockquote class="twitter-tweet" data-theme="{theme}">
<a href="https://x.com/Sion908_/status/{tweet_id}"></a>
</blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'''

        return [raw('', html, format='html')]


def setup(app):
    app.add_directive('twitter', TwitterDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
