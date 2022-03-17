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

// load file 
let loadFunc = async () => {
    
    // make request for messages
    let request = await fetch(`/chat-get-messages/${mailId}/`);
    let responce = await request.json();

    // work with responce
    
    
    /* 
    {% for i in mail_arr %}
                    {% if i.route_bool%}
                        <div class="message-container-from">
                            <span class="message">{{ i.body }}</span>
                        </div>
                    {% else %}
                        <div class="message-container-to">
                            <span class="message">{{ i.body }}</span>
                        </div>
                    {% endif %}
                {% endfor %}
    */
}

// send message to mail 
document.getElementById('push_btn').onclick = async () => {
    
    // get struct of data for sendins
    let requestData = await fetch('/chat-struct-for-message/', { 
        method: "POST", 
        headers: {
            "Content-Type": "application/json;charset=utf-8", 
            "X-CSRFToken": csrftoken 
        }, 
        body: JSON.stringify({ 
            id: '1'
        })
    });
    let resultData = await requestData.json();

    // get text from text_area
    let textArea = document.getElementById('floatingTextarea2').value;

    // send message by request
    let requestMessage = await fetch('/control-results-send-message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            text: textArea,
            mails: [resultData.mail], 
            request: resultData.request_id
        })
    });

    // work with components on page 
    
}
