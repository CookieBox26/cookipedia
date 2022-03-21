index=""
for filepath in *.html; do
    if [[ $filepath =~ index(_template)?\.html ]]; then
        continue
    fi
    title=`grep -e "<h1>" "$filepath"`
    title=${title#*<h1>}
    title=${title%</h1>*}
    ts=`date "+%Y-%m-%d" -r "$filepath"`
    index_="<li><a href=\""${filepath}"\">"${title}"</a>（最終更新日 "${ts}"）</li>"
    echo $index_
    index=${index}${index_}
done

sed -e "s@{{INDEX}}@$index@" index_template.html > index.html
sed -i -e "s@</li>@</li>\n@g" index.html
