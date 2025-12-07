import subprocess


if __name__ == '__main__':
    _run = lambda command: subprocess.run(command, capture_output=True, text=True, check=True)
    _run(['git', 'add', '.last_counts.toml'])
    _run(['git', 'add', 'add.py'])
    _run(['git', 'add', 'build.py'])
    _run(['git', 'add', 'docs/css/style.css'])
    _run(['git', 'add', 'docs/css/cookipedia.css'])
    _run(['git', 'add', 'docs/ja/articles/*'])
    _run(['git', 'add', 'docs/ja/categories/*'])
    _run(['git', 'add', 'docs/ja/index.html'])
    _run(['git', 'add', 'templates/ja/category_template.html'])
    _run(['git', 'add', 'templates/ja/index_template.html'])
    print(_run(['git', 'status', '-s']).stdout.rstrip('\n'))
