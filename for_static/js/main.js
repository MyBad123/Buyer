
//exit from profile
document.querySelector(".exit").onclick = async () => {
    let request = await fetch('/exit/');
    window.location.href = "/";
}



