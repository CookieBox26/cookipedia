#!/bin/bash

# カテゴリ一覧をここにかく --> カテゴリ一覧取得自動化のため廃止
# categories="
# categories/category_matrix.html=行列 
# categories/category_neurips_2021.html=NeurIPS&nbsp;2021 
# categories/category_transformer.html=Transformer 
# "

# 【注1】
# 各記事内で以下の形式の行を記述することでカテゴリの存在が認識され収集される。
# 現在カテゴリタイトル中の空白に未対応なので特殊文字にすること。
# <a href="../categories/category_transformer.html">Transformer</a> |
# <a href="../categories/category_neurips_2021.html">NeurIPS&nbsp;2021</a>

# 【注2】
# 逆に各記事内で行頭が <a であって category_xxx.html を含む行があるとき
# 「その記事がそのカテゴリに属する」と便宜上みなしている。
# 単に記事からカテゴリにリンクするときは a タグ開始位置を行頭にしないこと。


function collect_categories() {
    # 全記事からカテゴリ一覧を収集する
    # 収集結果は $categories に配列として格納する
    categories=""
    for filepath in articles/*.html; do
        category=`grep "/categories/category_" "$filepath"`
        if [[ -z $category ]]; then
            continue
        elif [[ ${category:0:2} != "<a" ]]; then
            continue
        fi
        category=${category//<a href=\"..\// }
        category=${category//<\/a>/ }
        category=${category//|/ }
        category=${category//\">/=}
        categories=${categories}${category}" "
    done
    categories=($categories)
    categories=($(for v in "${categories[@]}"; do echo "$v"; done | sort -u ))
    echo -e "\n===== カテゴリ収集結果 ====="
    for category in "${categories[@]}"; do
        echo $category
    done
}


function clear_category_files() {
    # カテゴリページを一旦全削除する
    for filepath in categories/*.html; do
        if [[ $filepath =~ .*_template.html ]]; then
            continue
        fi
        rm $filepath
    done
}


function create_category_files() {
    # 収集したカテゴリ一覧に基づきカテゴリページを再生成する
    for category in "${categories[@]}"; do
        category_title=${category#*=}
        category_url=${category%=*}
        n_index=0
        index=""
        for filepath in articles/*.html; do
            category_=`grep $category_url "$filepath"`
            if [[ -z $category_ ]]; then
                continue
            elif [[ ${category_:0:2} != "<a" ]]; then
                continue
            fi
            title=`grep "<h1>" "$filepath"`
            title=${title#*<h1>}
            title=${title%</h1>*}
            index_="<li><a href=\"../"${filepath}"\">"${title}"</a></li>"
            index=${index}${index_}
            n_index=$((n_index+1))
        done
        # そのカテゴリに紐づく記事が収集されたときだけカテゴリページを生成する
        if [[ -n $index ]]; then
            category_title=${category_title//&/\\&}  # sed の置換先のアンパサンドをエスケープ
            sed -e "s@{{CATEGORY_TITLE}}@$category_title@" categories/category_template.html > ${category_url}
            sed -i -e "s@{{CATEGORY_ARTICLE_LIST}}@$index@" ${category_url}
            sed -i -e "s@</li>@</li>\n@g" ${category_url}
            sed -i -e "s@{{NUM_OF_ARTICLES}}@$n_index@"  ${category_url}
        fi
    done
}


function create_index() {
    # 指定されたディレクトリ以下の全ページへのリンク列を生成する
    # 生成結果は $index に格納する
    echo -e "\n===== "${1}"以下のページ一覧 ====="
    n_index=0
    index=""
    for filepath in $1; do
        # _template が付くファイルはスキップ
        if [[ $filepath =~ .*_template.html ]]; then
            continue
        fi

        # 記事タイトルを抽出する
        title=`grep "<h1>" "$filepath"`
        title=${title#*<h1>}
        title=${title%</h1>*}
        title=${title//&/\\&}  # sed の置換先のアンパサンドをエスケープ

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
        n_index=$((n_index+1))
    done
}


collect_categories

clear_category_files

create_category_files

create_index "categories/*.html"
sed -e "s@{{CATEGORY_LIST}}@$index@" index_template.html > index.html
sed -i -e "s@{{NUM_OF_CATEGORIES}}@$n_index@" index.html

create_index "articles/*.html"
sed -i -e "s@{{ARTICLE_LIST}}@$index@" index.html
sed -i -e "s@{{NUM_OF_ARTICLES}}@$n_index@" index.html

sed -i -e "s@</li>@</li>\n@g" index.html
