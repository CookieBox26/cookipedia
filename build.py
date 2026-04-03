# /// script
# requires-python = "==3.11.*"
# dependencies = [
#     "cookies_site_utils",
# ]
# [tool.uv.sources.cookies_site_utils]
# git = "https://github.com/CookieBox26/cookies-site-utils"
# rev = "44d2d07b4acf16db97c4aa9784d9fdaf6bb90f55"
# ///
from cookies_site_utils.resources import sync_resource
from cookies_site_utils.builder import build_index, IndexPage, find_disallowed, Page
from pathlib import Path
import argparse
import logging


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force_keep_timestamp', action='store_true')
    args = parser.parse_args()

    work_root = Path(__file__).resolve().parent
    site_root = work_root / 'docs'
    sync_resource(site_root / 'css/style.css')
    sync_resource(site_root / 'funcs.js')

    with build_index(
        site_root,
        last_counts_path=(work_root / '.last_counts.toml'),
        force_keep_timestamp=args.force_keep_timestamp,
    ):
        _ = IndexPage(
            site_root,
            work_root / 'templates',
            'Cookipedia α-version',
        )

        targets = set()
        for rel_path in Page.last_counts.keys():
            if not (site_root / rel_path).is_file():
                logging.info('Not exist: ' + rel_path)
                targets.add(rel_path)
        Page.last_counts = {
            k: v for k, v in Page.last_counts.items()
            if k not in targets
        }

    find_disallowed(site_root, allowlist=[
        'funcs.js',
        'css/*.css',
        'index.html',
        'categories/*.html',
        'articles/*.html',
        'utils/*.html',
    ])
