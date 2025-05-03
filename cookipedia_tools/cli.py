from cookies_backpack.text_editor_interface import TextEditorInterface
import subprocess
import argparse
import os
import glob


def open_article(text_editor, browser, article_dir, article):
    article_fullpath = os.path.join(article_dir, article.strip())
    subprocess.Popen([text_editor, article_fullpath])
    subprocess.Popen([browser, article_fullpath])


def create_new_article(tei, browser, article_dir):
    def func(apple=200, banana=100):
        return apple + banana
    tei.run_with_args(func, {'apple': 200, 'banana': 100}, confirm=False)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--search', action='store_true')
    group.add_argument('-n', '--new', action='store_true')
    parser.add_argument('-k', '--keyword', type=str, default='')  # for search
    args = parser.parse_args()

    true_flags = sum([args.search, args.new])
    if true_flags != 1:
        parser.print_help()
        return

    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
    article_dir = os.path.join(root_dir, 'articles')
    log_file = os.path.join(root_dir, 'log.txt')
    text_editor = 'C:\\Program Files (x86)\\sakura\\sakura.exe'
    browser = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    tei = TextEditorInterface(log_file=log_file, text_editor=text_editor)

    if args.search:
        articles = glob.glob(os.path.join(article_dir, '*.html'))
        articles = [os.path.basename(article) for article in articles]
        articles = [article for article in articles if args.keyword in article]
        for article in articles:
            print(article)
        if len(articles) == 1:
            open_article(text_editor, browser, article_dir, articles[0])

    if args.new:
        create_new_article(tei, browser, article_dir)
