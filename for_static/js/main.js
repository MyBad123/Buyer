//create page
document.querySelector('.new-request').onclick = () => {
    window.location.href = '/user-new-request-page/';
}

//exit from profile
document.querySelector(".exit").onclick = async () => {
    let request = await fetch('/exit/');
    window.location.href = "/";
}



