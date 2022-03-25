# 記事一覧を生成する
index=""
for filepath in *.html; do
    # index.html と index_template.html はスキップする
    if [[ $filepath =~ index(_template)?\.html ]]; then
        continue
    fi

    # 記事タイトルを抽出する
    title=`grep -e "<h1>" "$filepath"`
    title=${title#*<h1>}
    title=${title%</h1>*}

    # 最終更新日付を取得する
    # git status コマンドの結果が空でないならファイルのタイムスタンプを,
    # git status コマンドの結果が空なら git log の最終更新日を参照する
    status=`git status -s "$filepath"`
    if [[ -n $status ]]; then
        ts=`date "+%Y-%m-%d" -r "$filepath"`
    else
        ts=`git log -1 --format="%ad" --date=short "$filepath"`
    fi

    index_="<li><a href=\""${filepath}"\">"${title}"</a><span class=\"index-ts\">（最終更新日 "${ts}"）</span></li>"
    echo $index_
    index=${index}${index_}
done

sed -e "s@{{INDEX}}@$index@" index_template.html > index.html
sed -i -e "s@</li>@</li>\n@g" index.html
