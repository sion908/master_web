from urllib.parse import urlparse
from html.parser import HTMLParser
from docutils.parsers.rst import Directive, directives
from docutils.nodes import raw
import requests


class _OGPHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self._in_title = False
        self.meta = {}

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
            return

        if tag != "meta":
            return

        attrs_dict = dict(attrs)
        key = attrs_dict.get("property") or attrs_dict.get("name")
        content = attrs_dict.get("content")
        if key and content:
            self.meta[key] = content

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


class OGPCardDirective(Directive):
    """OGP情報を取得してリンクカードを生成するディレクティブ"""

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False

    option_spec = {
        'title': directives.unchanged,
        'description': directives.unchanged,
        'image': directives.unchanged,
        'site_name': directives.unchanged,
    }

    def run(self):
        url = self.arguments[0]

        # オプションでOGP情報が指定されている場合はそれを使用
        if self.options:
            ogp_data = {
                'title': self.options.get('title') or url,
                'description': self.options.get('description') or '',
                'image': self.options.get('image') or '',
                'site_name': self.options.get('site_name') or urlparse(url).netloc,
                'url': url
            }
        else:
            # OGP情報を取得
            ogp_data = self.fetch_ogp(url)

        # HTML生成
        html = self.generate_card_html(url, ogp_data)

        return [raw('', html, format='html')]

    def fetch_ogp(self, url):
        """URLからOGP情報を取得"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, timeout=10, headers=headers)
            response.raise_for_status()
            response.encoding = response.apparent_encoding

            parser = _OGPHTMLParser()
            parser.feed(response.text)
            parser.close()

            og_title = parser.meta.get('og:title')
            og_description = parser.meta.get('og:description') or parser.meta.get('description')
            og_image = parser.meta.get('og:image')
            og_site_name = parser.meta.get('og:site_name')

            # フォールバック
            title = og_title or (parser.title.strip() if parser.title.strip() else url)
            description = og_description or ''
            image = og_image or ''
            site_name = og_site_name or urlparse(url).netloc

            ogp_data = {
                'title': title.strip() if title else url,
                'description': description.strip() if description else '',
                'image': image.strip() if image else '',
                'site_name': site_name.strip() if site_name else urlparse(url).netloc,
                'url': url
            }

            return ogp_data
        except Exception as e:
            print(f"OGP取得エラー: {url} - {e}")
            return {
                'title': url,
                'description': '',
                'image': '',
                'site_name': urlparse(url).netloc,
                'url': url
            }

    def get_meta_content(self, soup, property_name):
        """metaタグのcontentを取得"""
        meta = soup.find('meta', property=property_name) or soup.find('meta', attrs={'name': property_name})
        return meta.get('content') if meta else None

    def generate_card_html(self, url, ogp_data):
        """OGPカードのHTMLを生成"""
        image_html = ''
        if ogp_data['image']:
            image_html = f'''
            <div class="ogp-card-image">
                <img src="{ogp_data['image']}" alt="{ogp_data['title']}" loading="lazy">
            </div>'''

        description = ogp_data['description'][:200] + '...' if len(ogp_data['description']) > 200 else ogp_data['description']

        html = f'''
<a href="{url}" target="_blank" rel="noopener" class="ogp-card">
    <div class="ogp-card-content">
        {image_html}
        <div class="ogp-card-info">
            <div class="ogp-card-site">{ogp_data['site_name']}</div>
            <div class="ogp-card-title">{ogp_data['title']}</div>
            {f'<div class="ogp-card-description">{description}</div>' if description else ''}
        </div>
    </div>
</a>'''

        return html


def setup(app):
    app.add_directive('ogp-card', OGPCardDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
