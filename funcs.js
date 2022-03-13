function createIndex() {
    var index = '';
    var allHeaders = document.getElementsByTagName('h3');
    for (var i=0; i<allHeaders.length; ++i) {
        index += '<p><a href="#head' + String(i) + '">' + allHeaders[i].textContent + '</a></p>';
        allHeaders[i].innerHTML += '<a id="head' + String(i) + '"></a>';
    }
    document.getElementById('headers').innerHTML = index;
}
function contact() {
    var gitHub = '<a href="https://github.com/CookieBox26/memo/issues">Issues</a>';
    var message = 'お気付きの点がありましたら ' + gitHub + ' までご連絡ください。';
    var allContacts = document.getElementsByClassName('contact');
    for (var i=0; i<allContacts.length; ++i) {
        allContacts[i].innerHTML += message;
    }
}
function init() {
    contact();
    createIndex();
}
