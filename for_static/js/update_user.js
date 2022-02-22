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

//func for login input
if (document.querySelector(".input_login").value !== "") {
    document.querySelector(".span_login").style.opacity = "1";
}

document.querySelector(".input_login").addEventListener('focus', () => {
    let spanLogin = document.querySelector(".span_login") ;
    spanLogin.style.opacity = "1";
    spanLogin.style.color = "#000";
    spanLogin.innerHTML = "Логин";
})
document.querySelector(".input_login").addEventListener('blur', () => {
    if (document.querySelector(".input_login").value === "") {
        let spanLogin = document.querySelector(".span_login");
        spanLogin.style.opacity = "0";
    }
})

//func for password input
document.querySelector(".input_password").addEventListener('focus', () => {
    let spanPassword = document.querySelector(".span_password") ;
    spanPassword.style.opacity = "1";
})
document.querySelector(".input_password").addEventListener('blur', () => {
    if (document.querySelector(".input_password").value === "") {
        let spanPassword = document.querySelector(".span_password");
        spanPassword.style.opacity = "0";
    }
})

//push new user
let lastName = document.querySelector(".input_login").value;

document.querySelector(".auth_btn").addEventListener('click', async () => {
    let btnObject = document.querySelector(".auth_btn");
    btnObject.innerHTML = "загрузка";


    let response = await fetch('/update-user/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            "old_name": lastName,
            "new_name": document.querySelector(".input_login").value,
            "password": document.querySelector(".input_password").value
        })
    })

    if (response.ok) {
        document.querySelector(".input_password").value = "";
    }
    else {
        document.querySelector(".span_login").innerHTML = "Неправильный логин";
        document.querySelector(".span_login").style.color = "red";
    }

    lastName = document.querySelector(".input_login").value;
    btnObject.innerHTML = "обновить";

})





