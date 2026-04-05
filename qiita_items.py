"""
Qiita API から自分の Qiita 記事を取得・管理します。

### 使い方
```
python qiita_items.py -i  # 設定ファイルを新規作成する
python qiita_items.py -t TAG  # 指定タグの記事を検索する
python qiita_items.py -d  # キャッシュ -> 設定 TOML -> HTML の差分を表示する
python qiita_items.py -w  # 今週書いた記事を表示する
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
from pathlib import Path
from contextlib import suppress
import difflib
import keyring
import requests
import json
import argparse
import os
import re
import toml
import html
import datetime
import subprocess
from colorama import Fore
import logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def color_diff(diff):
    color = {'@': Fore.CYAN + '@'}
    for line in diff:
        yield color.get(line[0], line[0]) + line[1:] + Fore.RESET
        if line[0] == '@':
            color.update({'-': Fore.RED + '-', '+': Fore.GREEN + '+'})


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


def get_items(cache_file, force=False, user_id='CookieBox26'):
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

    Path(cache_file).parent.mkdir(parents=True, exist_ok=True)
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    return items


def item_to_line(item):
    return f'{item["id"]} {item["created_at"][:10]} {item["title"].strip()}'


def item_to_html(item):
    url = item['url']
    title = html.escape(item['title'].strip(), quote=False)
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
    logging.info(f'タグ検索します: {target_tags}')
    target_tags_lower = {tag.lower() for tag in target_tags}
    for item in items:
        tags = set([tag['name'].lower() for tag in item['tags']])
        if tags & target_tags_lower:
            print(item_to_line(item))


def show_cache_conf_diff(cache_file, toml_file, force=False, update=False):
    logging.info('キャッシュと設定ファイルの差分を確認します')
    items = get_items(cache_file, force)
    toml_text = Path(toml_file).read_text(encoding='utf8')
    cats = toml.loads(toml_text)['cats']
    id_to_item = {item['id']: item for item in items}
    updates = {}
    for key, s in cats.items():
        lines = s.strip().split('\n')
        if key == 'すべての記事':
            toml_ids = {line.split(' ', 1)[0] for line in lines}
            new_items = []
            for item in items:
                if item['id'] not in toml_ids:
                    print(f'[{key}] TOML にない:' + Fore.GREEN)
                    print(f'+ {item_to_line(item)}' + Fore.RESET)
                    new_items.append(item)
            if update and new_items:
                new_lines = [item_to_line(item) for item in new_items]
                updates[key] = '\n'.join(new_lines + lines) + '\n'
        else:
            cat_changed = False
            lines_ = []
            for line in lines:
                parts = line.split(' ', 2)
                item_id = parts[0]
                if item_id not in id_to_item:
                    raise ValueError(f'キャッシュにない記事: {item_id}')
                item = id_to_item[item_id]
                new_line = item_to_line(item)
                if new_line != line:
                    print(f'[{key}]')
                    print(Fore.RED + f'  - {line}' + Fore.RESET)
                    print(Fore.GREEN + f'  + {new_line}' + Fore.RESET)
                    lines_.append(new_line)
                    cat_changed = True
                else:
                    lines_.append(line)
            if update and cat_changed:
                updates[key] = '\n'.join(lines_) + '\n'
    if updates:
        for key, lines_ in updates.items():
            toml_text = re.sub(
                r'("' + re.escape(key) + r'")(\s*=\s*"""\n).*?(""")',
                lambda m, l=lines_: m.group(1) + m.group(2) + l + m.group(3),
                toml_text, flags=re.DOTALL,
            )
        Path(toml_file).write_text(toml_text, encoding='utf8', newline='\n')
        logging.info('設定ファイルを更新しました')


def show_conf_html_diff(cache_file, toml_file, html_file, update=False):
    logging.info('設定ファイルと HTML の差分を確認します')
    items = get_items(cache_file)
    cats = toml.loads(Path(toml_file).read_text(encoding='utf8'))['cats']
    html_text = Path(html_file).read_text(encoding='utf8')
    html_lines = html_text.splitlines()

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

    def print_diff(actual, expected, from_label, to_label):
        for line in color_diff(difflib.unified_diff(
            actual, expected, fromfile=from_label, tofile=to_label,
            lineterm='',
        )):
            print(line)

    # カテゴリ別の差分
    no_suffix = {'すべての記事', '作業効率化'}
    id_to_item = {item['id']: item for item in items}
    updates = []
    for key, s in cats.items():
        html_key = key if key in no_suffix else key + ' 関連'
        tag = 'h2' if key == 'すべての記事' else 'h3'
        li_lines = []
        for line in s.strip().split('\n'):
            item_id = line.split(' ', 1)[0]
            if item_id in id_to_item:
                li_lines.append(item_to_html(id_to_item[item_id]))
        expected = [f'<{tag}>{html_key}</{tag}>', '<ul>'] + li_lines + ['</ul>']
        actual = html_cats.get(html_key, [])
        print_diff(actual, expected, f'HTML ({html_key})', f'TOML ({key})')
        if update and actual and actual != expected:
            updates.append((actual, expected))
    if updates:
        for actual, expected in updates:
            html_text = html_text.replace('\n'.join(actual), '\n'.join(expected))
        Path(html_file).write_text(html_text, encoding='utf8', newline='\n')
        logging.info('HTML ファイルを更新しました')


def updates_this_week(today, items):
    if isinstance(today, str):
        today = datetime.datetime.strptime(today, '%Y%m%d').date()
    days_since_monday = today.weekday()  # monday=0, sunday=6
    monday = today - datetime.timedelta(days=days_since_monday)
    sunday = monday + datetime.timedelta(days=6)
    weekly_items = []
    for item in items:
        created_at = datetime.datetime.fromisoformat(
            item['created_at'].replace('Z', '+00:00'),
        )
        created_date = created_at.date()
        if monday <= created_date <= today:
            weekly_items.append((created_at, item))
    weekly_items.sort(key=lambda x: x[0])

    lines = [
        '今週は Qiita に以下の記事を書きました。',
        (
            'これまでに書いた記事一覧は'
            '[https://cookiebox26.github.io/cookipedia/'
            'utils/qiita_items.html:title=こちら]です。'
        ),
        '[:contents]',
        '<div class="h5-margin-bottom-02">',
    ]
    for _, item in weekly_items:
        title = html.escape(item['title'].strip(), quote=False)
        lines.append('*** ' + title)
        tags = ' '.join([
            '<span class="tag">' + tag['name'] + '</span>'
            for tag in item['tags']
        ])
        lines.append(tags)
        lines.append('[' + item['url'] + ':embed:cite]')
    lines.append('</div>')

    year, week, _ = sunday.isocalendar()
    subject = f'今週書いた Qiita 記事 ({year}年第{week}週)'
    print(sunday)
    print(subject)
    print('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force', action='store_true')
    parser.add_argument('--cache', default='.cache/qiita_items.json')
    parser.add_argument('--toml', default='.qiita_items.toml')
    parser.add_argument('--html', default='docs/utils/qiita_items.html')
    parser.add_argument(
        '--editor', default='C:\\Program Files (x86)\\sakura\\sakura.exe',
    )
    parser.add_argument('--today', default=None)
    parser.add_argument('-o', '--open', action='store_true')
    parser.add_argument('-u', '--update', action='store_true')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--init', action='store_true')
    group.add_argument('-t', '--tags', nargs='+')
    group.add_argument('-d', '--diff', action='store_true')
    group.add_argument('-w', '--week', action='store_true')

    args = parser.parse_args()

    if args.init:
        if os.path.exists(args.toml):
            logging.error(f'{args.toml} はすでに存在します')
            raise SystemExit(1)
        items = get_items(args.cache, args.force)
        lines = [item_to_line(item) for item in items]
        with open(args.toml, 'w', encoding='utf-8') as f:
            f.write('[cats]\n"すべての記事" = """\n')
            f.write('\n'.join(lines) + '\n"""\n')
    elif args.tags:
        items = get_items(args.cache, args.force)
        extract_ids_from_tag(set(args.tags), items)
    elif args.diff:
        show_cache_conf_diff(args.cache, args.toml, args.force, args.update)
        show_conf_html_diff(args.cache, args.toml, args.html, args.update)
    elif args.week:
        items = get_items(args.cache, args.force)
        today = args.today or datetime.datetime.now().date()
        updates_this_week(today, items)
    else:
        logging.warning('操作が指定されていません (-i/-t/-d/-w)')

    if args.open:
        subprocess.Popen([args.editor, args.toml])
        subprocess.Popen([args.editor, args.html])


if __name__ == '__main__':
    main()
