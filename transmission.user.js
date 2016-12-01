// ==UserScript==
// @match http://server.org:9091/transmission/web/
// ==/UserScript==
webserver_prefix = 'https://server.org/.priv8_bitch/';
hax = transmission.updateFromTorrentGet;
transmission.updateFromTorrentGet = function (a, b) {
    hax.apply(transmission, [a, b]);
    [].forEach.call(
        document.getElementsByClassName('torrent_name'),
        function (t) {
            if(t.innerHTML.search('<a') != 0) {
                t.innerHTML = '<a style="float:left ; right:0" target="_blank" href="' + webserver_prefix + t.innerText + '">Open ' + t.innerText + '</a>';
            }
        }
    );
};