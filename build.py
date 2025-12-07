# /// script
# requires-python = "==3.11.*"
# dependencies = [
#     "cookies_site_utils",
# ]
# [tool.uv.sources.cookies_site_utils]
# git = "https://github.com/CookieBox26/cookies-site-utils"
# rev = "e5283562e026142bbadd426ac08b94c9f319f746"
# ///
from pathlib import Path
from cookies_site_utils import index_generation, IndexPage, Sitemap, validate


if __name__ == '__main__':
    site_name = 'Cookipedia'
    work_root = Path(__file__).resolve().parent
    site_root = work_root / 'docs'
    style_css = site_root / 'css/style.css'
    funcs_js = site_root / 'funcs.js'
    lang_root = site_root / 'ja'
    lang_template_root = work_root / 'templates/ja'
    last_counts_path = work_root / '.last_counts.toml'

    with index_generation(
        site_name, site_root, style_css, funcs_js, last_counts_path, domain='',
        force_keep_timestamp=False,
    ):
        index_ja = IndexPage(lang_root, lang_template_root)
