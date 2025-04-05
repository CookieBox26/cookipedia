function prepareTitle() {
    var title = document.querySelectorAll('h1')[0].textContent;
    document.title = title + ' - Cookipedia';
}

function createSidebar(mainPage=false) {
    let content = '';

    if (!mainPage) {
        let gitHub = '<a href="https://github.com/CookieBox26/cookipedia/issues">Issues</a>';
        content += `<p>何かありましたら ${gitHub} までご連絡ください</p>`;
        let back = '<a href="../index.html">メインページに戻る</a>';
        content += '<p><a href="#">ページの一番上に戻る</a></p><p>' + back + '</p>';
        document.getElementById('smartphone-header').innerHTML += back;
    }

    const allHeaders = document.querySelectorAll('h2, h3');
    let index = '<h5>ページ内の小見出し一覧</h5>';
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
    content += `<div id="headers">${index}</div>`;

    if (mainPage) {
        let div = document.createElement('div');
        div.innerHTML = content;
        let ref = document.getElementById('header-quicklink');
        document.getElementById('sidebar').insertBefore(div, ref);
    } else {
        document.getElementById('sidebar').innerHTML += content;
    }
}

function setButton(id, handle) {
    let button = document.getElementById(id);
    button.addEventListener("click", handle);
    button.addEventListener("touchstart", handle);
}

function setButtonOpenClose(id0, id1) {
    let target = document.getElementById(id1);
    target.style.display = "none";
    setButton(id0, () => {
        target.style.display = (target.style.display == "none") ? "block" : "none";
    });
}

function init(mainPage=false) {
    if (!mainPage) prepareTitle();
    createSidebar(mainPage);

    const links = document.querySelectorAll('a');
    links.forEach((elem) => {
        const href = elem.getAttribute('href');
        if (href && href.startsWith('http')) {
            elem.setAttribute('target', '_blank');
            elem.setAttribute('rel', 'noopener noreferrer');
        }
    });
}
