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

// get id of request
function getIdRequest() {
    // get id for redirect and making request
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

// send message to mail
document.getElementById("push_btn").onclick = async () => {
    // get id of request
    let thisPk = getIdRequest();

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


// work with change of mail
for (let i of document.querySelectorAll('.input-mail')) {
    i.addEventListener('input', () => {
        // set and delete some class for settings new mail
        let btnChange = i.closest('.item').querySelector('.my-change-btn');
        btnChange.classList.add('btn');
        btnChange.classList.add('btn-primary');
        btnChange.classList.remove('opacity-0');
    })
}

for (let i of document.querySelectorAll('.my-change-btn')) {
    i.addEventListener('click', async () => {
        // make control what is this btn (with new mail or no)
        let forClass = 0;
        for (let j of i.classList) {
            if (j === 'opacity-0') {
                forClass++;
            }
        }

        // work after control
        if (forClass === 0) {
            // get data for request
            let textMail = i.closest('.item').querySelector('.input-mail').value;
            let textSite = i.closest('.item').querySelectorAll('td')[3].innerText;
            let idRequest = getIdRequest();

            // control valid or no textMail
            let forDog = 0;
            let forDot = 0;
            for (let j of textMail.slice('')) {
                if (j === '@') {
                    forDog++;
                }
                if (j === '.') {
                    forDot++;
                }
            }
            if (forDog === 0) {
                return
            }
            if (forDot === 0) {
                return
            }

            // set new request for change mail
            let request = await fetch('/request-page-change-mail/', {
                 method: 'POST',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        mail: textMail,
                        site: textSite,
                        id_request: idRequest
                    })
            })

            // change color and opacity for btn
            let responce = await request.json()
            console.log(responce);
        }
    })
}
