#!/bin/bash

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
    # 全記事から現在存在するカテゴリを収集する
    # 収集結果は $categories に配列として格納する
    # category_asymptotic_theory.html=漸近理論 category_matrix.html=行列 ...
    categories=""
    for filepath in articles/*.html; do
        # _template が付くファイルはスキップ
        if [[ $filepath =~ .*_template.html ]]; then
            continue
        fi
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
    # 収集したカテゴリのそれぞれに対してそのカテゴリに属する記事を再度集めて
    # カテゴリページを再生成する
    for category in "${categories[@]}"; do
        category_title=${category#*=}
        category_url=${category%=*}

        # 先に各ファイルの記事タイトルを抽出する (記事タイトルでソートするため)
        articles=""
        for filepath in articles/*.html; do
            # _template が付くファイルはスキップ
            if [[ $filepath =~ .*_template.html ]]; then
                continue
            fi
            category_=`grep $category_url "$filepath"`
            if [[ -z $category_ ]]; then
                continue
            elif [[ ${category_:0:2} != "<a" ]]; then
                continue
            fi

            # 記事タイトルを抽出する
            title=`grep "<h1>" "$filepath"`
            title=${title#*<h1>}
            title=${title%</h1>*}
            if [ -z "$title" ]; then
                title=`grep "^# " "$filepath"`
                title=${title#*\# }
            fi
            title=${title// /　}  # 空白があると上手くいかないので一旦全角に
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

            articles=${articles}${title}"="${filepath}"@"${ts}" "
        done
        articles=($articles)
        articles=($(for v in "${articles[@]}"; do echo "$v"; done | sort -f ))
        n_articles=${#articles[@]}

        n_index=0
        index=""
        for article in "${articles[@]:0:$n_articles}"; do
            title=${article%=*}
            title=${title//　/ }
            filepath=${article#*=}
            filepath=${filepath%@*}
            ts=${article#*@}

            index_="<a href=\"../"${filepath}"\">"${title}"</a>"
            if [[ $display_ts = "1" ]]; then
                index_=${index_}"<span class=\"index-ts\"> (最終更新日 "${ts}")</span>"
            fi
            echo $index_
            index=${index}"<li>"${index_}"</li>"
            n_index=$((n_index+1))
        done
        echo -e "\n----- "$category_title" のページ一覧 -----"
        echo $index

        # そのカテゴリに属する記事が収集されたときだけカテゴリページを生成する
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
    # ページ数は $n_index に格納する
    display_ts=$2  # 最終更新日を表示するか
    sort_ts=$3  # 更新日降順ソートにするか
    n_articles=$4  # 何件まで表示するか (0なら全て)

    # 先に各ファイルの記事タイトルを抽出する (記事タイトルでソートするため)
    articles=""
    for filepath in $1; do
        # _template が付くファイルはスキップ
        if [[ $filepath =~ .*_template.html ]]; then
            continue
        fi

        # 記事タイトルを抽出する
        title=`grep "<h1>" "$filepath"`
        title=${title#*<h1>}
        title=${title%</h1>*}
        if [ -z "$title" ]; then
            title=`grep "^# " "$filepath"`
            title=${title#*\# }
        fi
        title=${title// /　}  # 空白があると上手くいかないので一旦全角に
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

        articles=${articles}${title}"="${filepath}"@"${ts}" "
    done
    articles=($articles)
    if [[ $sort_ts = "1" ]]; then
        articles=($(for v in "${articles[@]}"; do echo "$v"; done | sort -r -k 2 -t @ ))
    else
        articles=($(for v in "${articles[@]}"; do echo "$v"; done | sort -f ))
    fi

    # 改めて各記事のリンクを書き出す
    echo -e "\n===== "${1}" 以下のページ一覧 ====="
    n_index=0
    index=""
    if [[ $n_articles = "0" ]]; then
        n_articles=${#articles[@]}
    fi
    for article in "${articles[@]:0:$n_articles}"; do
        title=${article%=*}
        title=${title//　/ }
        filepath=${article#*=}
        filepath=${filepath%@*}
        ts=${article#*@}

        index_="<a href=\""${filepath}"\">"${title}"</a>"
        if [[ $display_ts = "1" ]]; then
            index_=${index_}"<span class=\"index-ts\"> (最終更新日 "${ts}")</span>"
        fi
        echo $index_
        index=${index}"<li>"${index_}"</li>"
        n_index=$((n_index+1))
    done
}

# 全記事から現在存在するカテゴリを収集する
# 収集結果は $categories に配列として格納する
# category_asymptotic_theory.html=漸近理論 category_matrix.html=行列 ...
collect_categories

# カテゴリページを一旦全削除する
clear_category_files

# 収集したカテゴリのそれぞれに対してそのカテゴリに属する記事を再度集めて
# カテゴリページを再生成する
create_category_files

# categories/ 以下のページへのリンク列を生成する
create_index "categories/*.html" 0 0 0
# テンプレートに注入
sed -e "s@{{CATEGORY_LIST}}@$index@" index_template.html > index_.html
sed -i -e "s@{{NUM_OF_CATEGORIES}}@$n_index@" index_.html

# articles/ 以下のページへのリンク列を生成する
create_index "articles/*.html" 1 0 0
# テンプレートに注入
sed -i -e "s@{{ARTICLE_LIST}}@$index@" index_.html
sed -i -e "s@{{NUM_OF_ARTICLES}}@$n_index@" index_.html

# 更新日が新しい記事
create_index "articles/*.html" 1 1 10
sed -i -e "s@{{RECENT_ARTICLE_LIST}}@$index@" index_.html

# ブラウザ上の表示に影響ないがソースファイルで改行しておく
sed -i -e "s@</li>@</li>\n@g" index_.html

# 既存の index.html と行を並べ替えても不一致だったら上書き
diff <(sort index.html) <(sort index_.html) >/dev/null
if [ $? -eq 0 ]; then
    echo -e "\n行を入れ替えると差分がないので上書きしません"
    rm index_.html
else
    echo -e "\n行を入れ替えても差分があるので上書きします"
    mv index_.html index.html
fi
