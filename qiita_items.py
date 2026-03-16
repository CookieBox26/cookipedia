"""
Qiita API から自分の Qiita 記事を取得・管理します。

### 使い方
```
python qiita_items.py -f  # 強制的に新規取得する
python qiita_items.py -i  # 設定ファイルを新規作成する
python qiita_items.py -t TAG  # 指定タグの記事を検索する
python qiita_items.py -d  # 設定ファイルと HTML の差分を表示する
```

### 備考
Qiita のアクセストークンがあればまず認証ありでリクエストします。
Qiita のアクセストークンがある場合は以下で登録しておいてください。
```
python -c "$(cat <<'EOF'
import keyring
keyring.set_password('token@qiita', 'token', 'YOUR_TOKEN')
EOF
)"
```
Qiita のアクセストークンがあるかどうかは以下で確認してください。
```
python -c "$(cat <<'EOF'
import keyring
token = keyring.get_password('qiita', 'token')
print(token is not None)
EOF
)"
```
"""
from contextlib import suppress
import difflib
import keyring
import requests
import json
import argparse
import os
import re
import toml
import logging
from colorama import Fore, init
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
init(autoreset=True)


def fetch_all_pages(url, headers=None, params=None):
    items = []
    page = 1
    while True:
        p = {**(params or {}), 'per_page': 100, 'page': page}
        resp = requests.get(url, headers=headers, params=p)
        page_items = resp.json()
        if not isinstance(page_items, list) or len(page_items) == 0:
            break
        items.extend(page_items)
        if len(page_items) < 100:
            break
        page += 1
    return items


def get_items(
    force=False,
    cache_file='cache_qiita_items.json',
    user_id='CookieBox26',
):
    """
    Qiita API から自分のすべての Qiita 記事を取得します。

    Args:
        force: True ならキャッシュファイルがあっても強制的に新規取得
        cache_file: キャッシュファイルパス
        user_id: 自分の Qiita ユーザ ID (認証なしリクエストで使用)
    """
    if not force:
        logging.info('キャッシュファイルを確認します')
        with suppress(FileNotFoundError, json.JSONDecodeError):
            with open(cache_file, 'r', encoding='utf-8') as f:
                items = json.load(f)
            if isinstance(items, list):
                return items

    logging.info('最新の記事を取得します')
    items = None

    token = keyring.get_password('qiita', 'token')
    if token is not None:
        logging.info('認証ありでリクエストします')
        with suppress(requests.RequestException, ValueError):
            # https://qiita.com/api/v2/docs#get-apiv2authenticated_useritems
            url = 'https://qiita.com/api/v2/authenticated_user/items'
            headers = {'Authorization': f'Bearer {token}'}
            items = fetch_all_pages(url, headers=headers)

    if not isinstance(items, list) or len(items) == 0:
        logging.info('認証なしでリクエストします')
        # https://qiita.com/api/v2/docs#get-apiv2usersuser_iditems
        url = f'https://qiita.com/api/v2/users/{user_id}/items'
        items = fetch_all_pages(url)

    if not isinstance(items, list) or len(items) == 0:
        logging.error('記事の取得に失敗しました')
        return None

    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    return items


def item_to_str(item):
    url = item['url']
    title = item['title'].strip()
    date = item['created_at'][:10]
    tags = ' '.join([
        '<span class="tag">' + tag['name'] + '</span>'
        for tag in item['tags']
    ])
    return (
        '<li>'
        f'<a href="{url}">{title}</a>'
        f' {tags} <span class="index-ts-c">{date}</span>'
        '</li>'
    )


def extract_ids_from_tag(target_tags, items):
    for item in items:
        tags = set([tag['name'] for tag in item['tags']])
        if tags & target_tags:
            date = item['created_at'][:10]
            print(item['id'], date, item['title'].strip())


def show_cache_conf_diff(cats, items):
    logging.info('キャッシュと設定ファイルの差分を確認します')
    id_to_item = {item['id']: item for item in items}
    for key, s in cats.items():
        lines = s.strip().split('\n')
        if key == 'すべての記事':
            toml_ids = {line.split(' ', 1)[0] for line in lines}
            for item in items:
                if item['id'] not in toml_ids:
                    date = item['created_at'][:10]
                    print(f'[{key}] キャッシュにあるが TOML にない:')
                    print(Fore.GREEN + f'  + {item["id"]} {date} {item["title"]}')
            continue
        for line in lines:
            parts = line.split(' ', 2)
            item_id = parts[0]
            if item_id not in id_to_item:
                continue
            item = id_to_item[item_id]
            date = item['created_at'][:10]
            new_line = f'{item_id} {date} {item["title"]}'.strip()
            if new_line != line:
                print(f'[{key}]')
                print(Fore.RED + f'  - {line}')
                print(Fore.GREEN + f'  + {new_line}')


def show_conf_html_diff(cats, items, html_file):
    logging.info('設定ファイルと HTML の差分を確認します')
    with open(html_file, 'r', encoding='utf-8') as f:
        html_lines = f.readlines()

    # HTML からカテゴリごとのセクションを抽出
    html_cats = {}
    current_key = None
    in_ul = False
    for line in html_lines:
        line = line.rstrip('\n')
        m = re.match(r'^(<h[23]>.*?</h[23]>)$', line)
        if m:
            current_key = re.sub(r'^<h[23]>(.*?)</h[23]>$', r'\1', line)
            html_cats[current_key] = [line]
            in_ul = False
        elif line == '<ul>' and current_key is not None:
            in_ul = True
            html_cats[current_key].append(line)
        elif line == '</ul>' and in_ul:
            html_cats[current_key].append(line)
            in_ul = False
            current_key = None
        elif in_ul:
            html_cats[current_key].append(line)

    id_to_item = {item['id']: item for item in items}

    def print_diff(actual, expected, from_label, to_label):
        diff = list(difflib.unified_diff(
            actual, expected,
            fromfile=from_label,
            tofile=to_label,
            lineterm='',
        ))
        if diff:
            for line in diff:
                if line.startswith('-'):
                    print(Fore.RED + line)
                elif line.startswith('+'):
                    print(Fore.GREEN + line)
                else:
                    print(line)

    # カテゴリ別の差分
    no_suffix = {'すべての記事', '作業効率化'}
    for key, s in cats.items():
        html_key = key if key in no_suffix else key + ' 関連'
        tag = 'h2' if key == 'すべての記事' else 'h3'
        li_lines = []
        for line in s.strip().split('\n'):
            item_id = line.split(' ', 1)[0]
            if item_id in id_to_item:
                li_lines.append(item_to_str(id_to_item[item_id]))
        expected = [f'<{tag}>{html_key}</{tag}>', '<ul>'] + li_lines + ['</ul>']
        actual = html_cats.get(html_key, [])
        print_diff(actual, expected, f'HTML ({html_key})', f'TOML ({key})')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force', action='store_true')
    parser.add_argument('--cache', default='.cache/qiita_items.json')
    parser.add_argument('--toml', default='.qiita_items.toml')
    parser.add_argument('--html', default='docs/utils/qiita_items.html')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--init', action='store_true', help='設定新規作成')
    group.add_argument('-t', '--tags', nargs='+', help='タグ検索')
    group.add_argument('-d', '--show_diff', action='store_true', help='差分表示')
    args = parser.parse_args()

    items = get_items(args.force, cache_file=args.cache)
    if args.init:
        if os.path.exists(args.toml):
            logging.error(f'{args.toml} はすでに存在します')
            raise SystemExit(1)
        lines = [
            f'{item["id"]} {item["created_at"][:10]} {item["title"].strip()}'
            for item in items
        ]
        with open(args.toml, 'w', encoding='utf-8') as f:
            f.write('[cats]\n"すべての記事" = """\n')
            f.write('\n'.join(lines))
            f.write('\n"""\n')
    elif args.tags:
        extract_ids_from_tag(set(args.tags), items)
    elif args.show_diff:
        with open(args.toml, 'r', encoding='utf-8') as f:
            cats = toml.load(f)['cats']
        show_cache_conf_diff(cats, items)
        show_conf_html_diff(cats, items, html_file=args.html)


if __name__ == '__main__':
    main()
