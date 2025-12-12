# /// script
# requires-python = "==3.11.*"
# dependencies = [
#     "cookies_site_utils",
# ]
# [tool.uv.sources.cookies_site_utils]
# git = "https://github.com/CookieBox26/cookies-site-utils"
# rev = "2a8229580bc1c7192925c0dd88166a8633a24d52"
# ///
from pathlib import Path
from cookies_site_utils import index_generation, IndexPage, Sitemap, validate


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
        index_cookipedia = IndexPage(site_root)
        index_cookipedia.build(work_root / 'templates', 'Cookipedia α-version')
