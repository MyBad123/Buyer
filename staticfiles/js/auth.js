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

//for login-input
let loginInputFocus = (e) => {
    document.querySelector(".span_login").style.opacity = "1";
    e.target.placeholder = "";
}
let loginInputBlur = (e) => {
    inputValue = document.querySelector(".input_login").value

    if (inputValue === "") {
        document.querySelector(".span_login").style.opacity = "0";
        e.target.placeholder = "Логин";
    }
}

//for password-input
let paswordInputFocus = (e) => {
    document.querySelector(".span_password").style.opacity = "1";
    document.querySelector(".span_password").style.color = "#000";
    e.target.placeholder = "";
}
let passwordInputBlur = (e) => {
    inputValue = document.querySelector(".input_password").value

    if (inputValue === "") {
        document.querySelector(".span_password").style.opacity = "0";
        e.target.placeholder = "Пароль";
    }
}

//for auth btn
let autnBtnClick = async () => {
    //open loader
    document.querySelector(".load").classList.add("for_load");

    //push request
    let request = await fetch('/auth/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            "login": document.querySelector(".input_login").value,
            "password": document.querySelector(".input_password").value
        })
    })
    let result = await request.json();

    if (request.ok) {
        window.location.href = "/user-page/";
    } else {
        spanPasswrod = document.querySelector(".span_password");
        spanPasswrod.style.color = "red";
        spanPasswrod.innerHTML = "Неправильный пароль";
    }

    //close preloader
    setTimeout(() => {
        document.querySelector(".load").classList.remove("for_load");
    }, 2000);
}

//event for forget password
forgetBtnEvent = () => {
    document.querySelector(".content").innerHTML = `
                <p class="reg_word">Восстановить пароль</p>
                <div class="container_input">
                    <input type="text" class="form-control input_mail">
                    <span class="span_mail">Почта</span>
                </div>
                <p class="mail_btn btn btn-primary">Войти</p>
                <p class="no_forget_passwrod">Отмена</p>
            `
    document.querySelector(".no_forget_passwrod").addEventListener('click', cancelBtnEvent);
}

//event for cancel btn
cancelBtnEvent = () => {
    document.querySelector(".content").innerHTML = `
                <p class="reg_word">Регистрация</p>
                <div class="container_input">
                    <input type="text" class="form-control input_login" placeholder="Логин">
                    <span class="span_login">Логин</span>
                </div>
                <div class="container_input">
                    <input type="password" class="form-control input_password" placeholder="Пароль">
                    <span class="span_password">Пароль</span>
                </div>
                <p class="auth_btn btn btn-primary">Войти</p>
                <p class="forget_passwrod">Забыли пароль?</p>
            `;

    //event for input login
    let inputLogin = document.querySelector(".input_login");
    inputLogin.addEventListener('focus', loginInputFocus);
    inputLogin.addEventListener('blur', loginInputBlur);

    //event for input password
    let inputPassword = document.querySelector(".input_password");
    inputPassword.addEventListener('focus', paswordInputFocus);
    inputPassword.addEventListener('blur', passwordInputBlur);

    //event for push btn
    let btnAuth = document.querySelector(".auth_btn");
    btnAuth.addEventListener('click', autnBtnClick);

    //event for forget btn
    let btnForget = document.querySelector(".forget_passwrod");
    btnForget.addEventListener('click', forgetBtnEvent);
}

document.querySelector(".forget_passwrod").addEventListener('click', () => {
    document.querySelector(".content").innerHTML = `
                <p class="reg_word">Восстановить пароль</p>
                <div class="container_input">
                    <input type="text" class="form-control input_mail">
                    <span class="span_mail">Почта</span>
                </div>
                <p class="mail_btn btn btn-primary">Войти</p>
                <p class="no_forget_passwrod">Отмена</p>
            `
    document.querySelector(".no_forget_passwrod").addEventListener('click', cancelBtnEvent);
})

document.querySelector(".input_login").addEventListener('focus', loginInputFocus);
document.querySelector(".input_login").addEventListener('blur', loginInputBlur);

document.querySelector(".input_password").addEventListener('focus', paswordInputFocus);
document.querySelector(".input_password").addEventListener('blur', passwordInputBlur);

document.querySelector(".auth_btn").addEventListener("click", autnBtnClick);