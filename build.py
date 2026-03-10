# /// script
# requires-python = "==3.11.*"
# dependencies = [
#     "cookies_site_utils",
# ]
# [tool.uv.sources.cookies_site_utils]
# git = "https://github.com/CookieBox26/cookies-site-utils"
# rev = "1d31318ba565f7028528316f6b8f7e32bf328886"
# ///
from pathlib import Path
from cookies_site_utils import index_generation, IndexPage, validate


if __name__ == '__main__':
    work_root = Path(__file__).resolve().parent
    site_root = work_root / 'docs'
    style_css = site_root / 'css/style.css'
    funcs_js = site_root / 'funcs.js'
    last_counts_path = work_root / '.last_counts.toml'

    with index_generation(
        site_root, style_css, funcs_js, last_counts_path, domain='',
        force_keep_timestamp=False,
    ):
        # クッキペディアインデックスページ生成
        index_cookipedia = IndexPage(site_root)
        index_cookipedia.build(work_root / 'templates', 'Cookipedia α-version')
        validate(
            site_root,
            ['funcs.js', 'index.html'],  # 存在してよいファイル
            ['css', 'articles', 'categories', 'utils'],  # 存在してよいフォルダ
        )
