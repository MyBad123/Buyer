// get csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function getId() {
    let thisHrefBool = true;
    let index = -1;

    while (thisHrefBool) {
        index -= 1;
        if (window.location.href.slice(index, -1)[0] === '/') {
            thisHrefBool = false;
        }
    }
    let thisPk = window.location.href.slice(index + 1, -1);

    return thisPk
}

document.getElementById('push_btn').onclick = async () => {
    // add data for sending message
    let text = document.getElementById('floatingTextarea2').value;
    let idPage = getId();

    // send request
    let request = await fetch('/chat-get-send-message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            text: textMessage,
            mails: mailArrWithSite,
            request: thisPk
        })
    })
    if 
}