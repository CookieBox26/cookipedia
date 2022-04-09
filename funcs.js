function createSidebar() {
    var gitHub = '<a href="https://github.com/CookieBox26/cookipedia/issues">Issues</a>';
    var message = '何かありましたら ' + gitHub + ' までご連絡ください';

    var index = '<h5>このページの小見出し一覧</h5>';
    var allHeaders = document.querySelectorAll('h2, h3');
    for (var i=0; i<allHeaders.length; ++i) {
        index += '<p class="';
        if (allHeaders[i].tagName == 'H3') {
            index += 'indent';
        }
        index += '">';
        index += '<a href="#head' + String(i) + '">';
        index += allHeaders[i].textContent + '</a></p>';
        allHeaders[i].innerHTML += '<a id="head' + String(i) + '"></a>';
    }

    var content = '<p class="contact">' + message + '</p><br/>';
    var back = '<a href="../index.html">メインページに戻る</a>';
    content += '<p><a href="#">このページの一番上に戻る</a></p><p>' + back + '</p><br/>';
    content += '<div id="headers">' + index + '</div>';
    document.getElementById('sidebar-item').innerHTML += content;
    document.getElementById('smartphone-header').innerHTML += back;
}

function syntaxHighlight() {
    let pres = document.getElementsByTagName('pre');
    for (let i=0; i < pres.length; ++i) {
        let re = [];
        if (pres[i].classList.contains('python')) {
            // 文字列リテラル
            re.push([/([^"])(")([^"]*)(")([^"])/g, '$1<span__literal__>$2$3$4</span>$5']);
            re.push([/([^'])(')([^']*)(')([^'])/g, '$1<span__literal__>$2$3$4</span>$5']);
            // コメント
            re.push([/(#.*?)(<br\/>)/g, '<span__comment__>$1</span>$2']);
            re.push([/("""|''')(.*?)("""|''')/g, '<span__comment__>$1$2$3</span>']);
            // 数値
            re.push([/([+-]?[0-9]+[\.]?[0-9]?(?:[eE][+-]?[0-9]+)?)/g,
                     '<span__numeric__>$1</span>']);
            re.push([/(True|False|None)/g, '<span__numeric__>$1</span>']);
            // キーワード
            re.push([/(<br\/>|\s)(and|as|assert|async|await|break|class)(<br\/>|\s)/g,
                     '$1<span__keyword__>$2</span>$3']);
            re.push([/(<br\/>|\s)(continue|def|del|elif|else|except|finally|for)(<br\/>|\s)/g,
                     '$1<span__keyword__>$2</span>$3']);
            re.push([/(<br\/>|\s)(from|global|if|import|in|is|lambda|nonlocal|not)(<br\/>|\s)/g,
                     '$1<span__keyword__>$2</span>$3']);
            re.push([/(<br\/>|\s)(or|pass|raise|return|try|while|with|yield)(<br\/>|\s)/g,
                     '$1<span__keyword__>$2</span>$3']);
            // 組み込み関数
            re.push([/(<br\/>|\s)(abs|all|any|dict|enumerate|len|print|type)(\()/g,
                     '$1<span__builtin__>$2</span>$3']);
        }
        if (re.length == 0) {
            continue;
        }
        let code = pres[i].innerHTML;
        // 文頭・改行・文末を扱いやすくするためにすべて <br/> に置換する．
        code = '<br/>' + code.replace(/\n/g, '<br/>') + '<br/>';
        for (let i=0; i < re.length; ++i) {
            code = code.replace(re[i][0], re[i][1]);
        }
        code = code.replace(/span__(.*?)__/g, 'span class="$1"');
        code = code.replace(/^<br\/>/, '');
        code = code.replace(/<br\/>$/, '');
        pres[i].innerHTML = code;
    }
}

function init() {
    createSidebar();
    syntaxHighlight();
}
