//get csrf token
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

//delete users object
for (let i of document.querySelectorAll(".btn_delete")) {
    i.onclick = async (e) => {
        let valueLogin = e.target.closest(".align-items-center").querySelector(".col-form-label").innerHTML.substr(7);

        let request = await fetch("/delete-user/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                "login": valueLogin
            })
        })

        e.target.closest(".item").remove();
    }
}

//update users btn
for (let i of document.querySelectorAll(".btn_change")) {
    i.addEventListener('click', (e) => {
        let valueId = e.target.closest(".col-12").querySelector(".input_id").value;
        window.location.href = "/update-user-page/?id=" + valueId;
    })
}
