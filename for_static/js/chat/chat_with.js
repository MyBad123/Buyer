document.querySelector('.my-messages').scrollBy(0, 10000);

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

// get id of mail
let getIdMail = () => {
    let thisHrefBool = true;
    let index = -1;

    while (thisHrefBool) {
        index -= 1;
        if (window.location.href.slice(index, -1)[0] === '/') {
            thisHrefBool = false;
        }
    }

    return window.location.href.slice(index + 1, -1);
}
const mailId = getIdMail();