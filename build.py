# /// script
# requires-python = "==3.11.*"
# dependencies = [
#     "cookies_site_utils",
# ]
# [tool.uv.sources.cookies_site_utils]
# git = "https://github.com/CookieBox26/cookies-site-utils"
# rev = "8d42eaa355c5f54f0a440a65a9ce1e0f8f058276"
# ///
from cookies_site_utils.resources import sync_resource
from cookies_site_utils.builder import build_index, IndexPage, find_disallowed
from pathlib import Path


if __name__ == '__main__':
    work_root = Path(__file__).resolve().parent
    site_root = work_root / 'docs'
    sync_resource(site_root / 'css/style.css')
    sync_resource(site_root / 'funcs.js')

    with build_index(
        site_root,
        last_counts_path=(work_root / '.last_counts.toml'),
        force_keep_timestamp=False,
    ):
        _ = IndexPage(
            site_root,
            work_root / 'templates',
            'Cookipedia α-version',
        )

    find_disallowed(site_root, allowlist=[
        'funcs.js',
        'css/*.css',
        'index.html',
        'categories/*.html',
        'articles/*.html',
        'utils/*.html',
    ])
