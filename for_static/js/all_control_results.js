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

// send message to mail
document.getElementById("push_btn").onclick = async () => {
    // get id for redirect and making request
    let thisHrefBool = true;
    let index = -1;

    while (thisHrefBool) {
        index -= 1;
        if (window.location.href.slice(index, -1)[0] === '/') {
            thisHrefBool = false;
        }
    }
    let thisPk = window.location.href.slice(index + 1, -1);


    // get text by input area 
    let textMessage = document.getElementById('floatingTextarea2').value;
    if (textMessage === '') {
        return
    }

    // get mails for sending
    let mailArrWithSite = [];
    for (let i of document.querySelectorAll('.form-check-input')) {
        
        // if checkbox is true, add mail to arr
        if (i.checked) {
            mailName = i.closest(".item").querySelectorAll("td")[1].innerHTML;
            siteName = i.closest(".item").querySelectorAll("td")[2].innerHTML;
            
            // if mailArr has no mail, add it
            mailArrWithSite.push({
                'mail': mailName,
                'site': siteName
            })
        }
    }
    // control mailArr 
    if (mailArrWithSite.length === 0) {
        return
    }

    // send message by request
    let request = await fetch('/control-results-send-message/', {
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

    // redirect to thanks page 
    window.location.href = '/control-results-send-message-thanks/' + thisPk + '/';
}

