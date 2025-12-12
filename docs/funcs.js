function setModeButton(localStorageKeyName, elmId, mode) {
    document.getElementById(elmId).addEventListener('click', () => {
        document.documentElement.setAttribute('data-mode', mode);
        localStorage.setItem(localStorageKeyName, mode);
    });
}

function createModeButtons(i, lang) {
    let btns = '<div class="mode-container">';
    btns += (lang == 'ja') ? '配色切替' : 'Light/Dark';
    btns += `<div id="mode-light-${i}" class="mode-btn"></div>`;
    btns += `<div id="mode-dark-${i}" class="mode-btn"></div>`;
    btns += '</div>';
    return btns;
}

function createSidebar(repo = 'cookie-box', isIndex = false, linkTop = false, lang = 'ja') {
    let indexUrl = isIndex ? 'index.html' : '../index.html';
    let toIndex = `<a class="index-link" href="${indexUrl}"></a>`;
    let gitHub = `<a href="https://github.com/CookieBox26/${repo}/issues">Issues</a>`;
    let localStorageKeyName = (repo == 'cookie-box') ? 'mode' : `mode-${repo}`;

    let spHeaderLeft = isIndex ? '<span></span>' : toIndex;
    let modeButtons0 = createModeButtons(0, lang);
    let modeButtons1 = createModeButtons(1, lang);
    document.getElementById('smartphone-header').innerHTML += spHeaderLeft + modeButtons0;

    let content = '';
    content += `<h2 class="logo">${toIndex}</h2>`;
    content += `<p>${modeButtons1}</p>`;
    content += isIndex ? '' : `<p>ご指摘等は ${gitHub} までご連絡ください</p>`;
    content += isIndex ? '' : '<p><a href="#">ページの一番上に戻る</a></p>';

    const allHeaders = document.querySelectorAll('h2, h3');
    if (allHeaders.length > 0) {
        let index = '<h5>ページ内の小見出し一覧</h5>';
        for (var i = 0; i < allHeaders.length; ++i) {
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
    }

    if (isIndex) {
        let div = document.createElement('div');
        div.innerHTML = content;
        let ref = document.getElementById('bookmark');
        document.getElementById('sidebar').insertBefore(div, ref);
    } else {
        document.getElementById('sidebar').innerHTML += content;
    }
    if (linkTop) {
        let topUrl = isIndex ? '../index.html' : '../../index.html';
        let toTop = `From&nbsp;<a class="top-link" href="${topUrl}"></a>`;
        let toTopDiv = `<div class="top-link">${toTop}</div>`;
        document.getElementById('sidebar').innerHTML += toTopDiv;
        const footer = document.getElementById('smartphone-footer');
        if (footer) {
            footer.innerHTML += toTop;
        }
    }

    document.documentElement.setAttribute('data-mode', 'light');
    const saved = localStorage.getItem(localStorageKeyName);
    if (saved) document.documentElement.setAttribute('data-mode', saved);
    for (var i = 0; i < 2; ++i) {
        setModeButton(localStorageKeyName, `mode-light-${i}`, 'light');
        setModeButton(localStorageKeyName, `mode-dark-${i}`, 'dark');
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

function loadMathJax() {
    window.MathJax = {tex: {inlineMath: [['$', '$']]}};
    const script = document.createElement('script');
    script.src = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/4.0.0/tex-chtml.min.js";
    script.defer = true;
    script.crossOrigin = "anonymous";
    script.referrerPolicy = "no-referrer";
    script.integrity = "sha512-cHFHvgPwgoSbpMuTqgZCOWHzoFqt48aXErA98EcvAiZdN6v2bz416BjOqhZJ4tm+QzVkdeLY6NpEWYEjHBx49w==";
    document.head.appendChild(script);
}

function secureExternalLinks(root = document) {
    const originHost = location.host;
    root.querySelectorAll('a[href]').forEach((a) => {
        const href = a.getAttribute('href');
        if (!href) return;
        if (href.startsWith('#') || href.startsWith('mailto:')) return;
        const url = new URL(href, location.href);
        if (url.host === originHost) return;
        a.setAttribute('target', '_blank');
        const rel = (a.getAttribute('rel') || '').split(/\s+/);
        ['noopener', 'noreferrer'].forEach(v => {
            if (!rel.includes(v)) rel.push(v);
        });
        a.setAttribute('rel', rel.filter(Boolean).join(' '));
    });
}

function init(repo, isIndex = false, isTop = false, lang = 'ja') {
    createSidebar(repo, isIndex, isTop, lang);
    secureExternalLinks();
}

document.addEventListener('DOMContentLoaded', () => {
    const s = document.getElementById('app');
    const repo = s?.dataset.repo || 'cookie-box';
    const isIndex = s?.dataset.isIndex === 'true';
    const linkTop = s?.dataset.linkTop === 'true';
    const lang = s?.dataset.lang || 'ja';
    init(repo, isIndex, linkTop, lang);
    if (s?.dataset.mathjax === 'true') loadMathJax();
});

(function () {
    if (typeof Prism === 'undefined' || typeof document === 'undefined') return;
    Prism.hooks.add('before-sanity-check', function (env) {
        env.code = env.code.replace(/^(?:\r?\n|\r)/, '');
    });
})();
