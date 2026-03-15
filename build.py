# /// script
# requires-python = "==3.11.*"
# dependencies = [
#     "cookies_site_utils",
# ]
# [tool.uv.sources.cookies_site_utils]
# git = "https://github.com/CookieBox26/cookies-site-utils"
# rev = "1e2db74afb9eb3402646dab686cd1d3b5c9a3801"
# ///
from cookies_site_utils.builder import build_index, IndexPage, validate
from pathlib import Path
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
)


if __name__ == '__main__':
    work_root = Path(__file__).resolve().parent
    site_root = work_root / 'docs'
    style_css = site_root / 'css/style.css'
    funcs_js = site_root / 'funcs.js'
    last_counts_path = work_root / '.last_counts.toml'

    with build_index(
        site_root, style_css, funcs_js, last_counts_path,
        force_keep_timestamp=False,
    ):
        _ = IndexPage(
            site_root,
            work_root / 'templates',
            'Cookipedia α-version',
        )
        validate(
            site_root,
            ['funcs.js', 'index.html'],
            ['css', 'articles', 'categories', 'utils'],
        )
