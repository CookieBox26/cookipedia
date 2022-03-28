#!/bin/bash

# カテゴリ一覧をここにかく
# ※ 各記事のカテゴリリンクもこれに同期しないとカテゴリ一覧に吸い上げできない
# ※ カテゴリを廃止してここから削除した場合にカテゴリページ削除やカテゴリリンク削除はなされない
categories="
href=\"../categories/category_matrix.html\">行列 
"
categories="$categories"


function create_categories() {
    # カテゴリページを生成する
    for category in $categories; do
        index=""
        for filepath in articles/*.html; do
            category_=`grep -e $category "$filepath"`
            if [[ -n $category_ ]]; then
                title=`grep -e "<h1>" "$filepath"`
                title=${title#*<h1>}
                title=${title%</h1>*}
                index_="<li><a href=\"../"${filepath}"\">"${title}"</a></li>"
                index=${index}${index_}
            fi
        done
        # そのカテゴリに紐づく記事が収集されたときだけカテゴリページを生成する
        if [[ -n $index ]]; then
            category_title=${category#*>}
            category_url=${category#*category_}
            category_url=${category_url%.html*}
            sed -e "s@{{CATEGORY_TITLE}}@$category_title@" categories/category_template.html > categories/category_${category_url}.html
            sed -i -e "s@{{CATEGORY_ARTICLE_LIST}}@$index@" categories/category_${category_url}.html
        fi
    done
}


function create() {
    # 指定されたディレクトリ以下のページ一覧を収集する
    index=""
    for filepath in $1; do
        # _template が付くファイルはスキップ
        if [[ $filepath =~ .*_template.html ]]; then
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
}


create_categories

create "categories/*.html"
sed -e "s@{{CATEGORY_LIST}}@$index@" index_template.html > index.html

create "articles/*.html"
sed -i -e "s@{{ARTICLE_LIST}}@$index@" index.html

sed -i -e "s@</li>@</li>\n@g" index.html
