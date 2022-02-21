
//exit from profile
document.querySelector(".exit").onclick = async () => {
    let request = await fetch('/exit/');
    window.location.href = "/";
}

for (let i of document.querySelectorAll('.item')) {
    i.onclick = (e) => {
        e.target.closest('.item').querySelector('.item-ref')
    }
}

