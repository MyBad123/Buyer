//get token
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

//exit from profile
document.querySelector(".exit").onclick = async () => {
    let request = await fetch('/exit/');
    window.location.href = "/";
}

//new request
document.querySelector('.btn-request').onclick = async () => {
    if (document.querySelector('.input-request').value !== '') {
        let request = await fetch('/user-new-request/', {
            method: "POST",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                "request": document.querySelector('.input-request').value
            })
        })
        let response = await request.json();
        if (request.ok) {
            document.querySelector('.input-request').value = '';
            document.querySelector('.table-content').insertAdjacentHTML(
                'afterBegin',
                `
                    <td>${response.name}</td>
                    <td>${response.date_creation}</td>
                    <td>${response.status}</td>
                    <td>${response.user}</td>
                `
            );
        }
        document.querySelector('.input-request').value = '';
    }
}

