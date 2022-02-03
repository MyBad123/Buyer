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
        let valueLogin = e.target.closest(".content_item").querySelector(".p_login").innerHTML;


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

        e.target.closest(".content_item").remove();


    }
}

btnDeleteEvent = async (e) => {
    let deleteObject = e.target.closest(".content_item");
    let deleteName = deleteObject.innerHTML;
    deleteObject.remove();

    //remove object from bd
    let request = await fetch('/delete-user/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            "login": deleteName
        })
    })
}

//update users btn
for (let i of document.querySelectorAll(".btn_change")) {
    i.addEventListener('click', (e) => {
        let valueId = e.target.closest(".btns").querySelector(".input_id").value;
        window.location.href = "/update-user-page/?id=" + valueId;
    })
}

//create users object
document.querySelector(".add_btn").addEventListener("click", () => {
    window.location.href = "/user-add-page/";
});

//go to user's list
document.querySelector(".menu_users").onclick = () => {
    window.location.href = "/user-page/";
}

//go to btn for delete db
document.querySelector(".menu_db").onclick = () => {
    window.location.href = "/db/";
}

//exit from admin panel
document.querySelector(".menu_exit").onclick = async () => {
    let request = await fetch("/exit/");
    window.location.href = "/";
}