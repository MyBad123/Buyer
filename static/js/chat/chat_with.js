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

// load file 
let loadFunc = async () => {
    
    // make request for messages
    let request = await fetch(`/chat-get-messages/${mailId}/`);
    let responce = await request.json();

    // work with responce
    for (let i of responce.messages) {
        
        // work with route
        let routeStruct;
        if (i.route_to_bool) {
            // if company send to me message
            routeStruct = {
                container: 'message-container-to',
                containerMessageTime: 'message-container-to-container'
            }
        } 
        else {
            // if we send to company message 
            routeStruct = {
                container: 'message-container-from',
                containerMessageTime: 'message-container-from-container'
            }
        }

        // work with string
        let strDiv = `
            <div class="${routeStruct.container}">
                <div class="${routeStruct.containerMessageTime}">
                    <span class="message">${i.body}</span>
                    <span class="message-time">${i.datetime}</span>
                </div>
            </div>
        `

        // add this str to html 
        document.querySelector('.messages-container').insertAdjacentHTML('beforeend', strDiv);

        // scroll messages 
        document.querySelector('.my-messages').scrollBy(0, 10000);
    }
}
loadFunc();

// send message to mail 
document.getElementById('push_btn').onclick = async () => {
    
    // work with request 
    let text = document.getElementById('floatingTextarea2').value;

    

    // work with string
    let strDiv = `
        <div class="message-container-from">
            <div class="message-container-from-container">
                <span class="message">${text}</span>
                <span class="message-time">2022-03-17T13:42:09.820Z</span>
            </div>
        </div>
    `

    // add this str to html 
    document.querySelector('.messages-container').insertAdjacentHTML('beforeend', strDiv);

    // scroll messages 
    document.querySelector('.my-messages').scrollBy(0, 10000);

    // clear message
    document.getElementById('floatingTextarea2').value = '';
}
