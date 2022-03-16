function createSidebar() {
    var gitHub = '<a href="https://github.com/CookieBox26/memo/issues">Issues</a>';
    var message = '何かありましたら ' + gitHub + ' までご連絡ください';

    var index = '<h5>このページの小見出し一覧</h5>';
    var allHeaders = document.getElementsByTagName('h2');
    for (var i=0; i<allHeaders.length; ++i) {
        index += '<p><a href="#head' + String(i) + '">' + allHeaders[i].textContent + '</a></p>';
        allHeaders[i].innerHTML += '<a id="head' + String(i) + '"></a>';
    }

    var content = '<p class="contact">' + message + '</p><br/>';
    var back = '<a href="index.html">メインページに戻る</a>';
    content += '<p><a href="#">このページの一番上に戻る</a></p><p>' + back + '</p><br/>';
    content += '<div id="headers">' + index + '</div>';
    document.getElementById('sidebar-item').innerHTML += content;
    document.getElementById('smartphone-header').innerHTML += back;
}
function init() {
    createSidebar();
}
