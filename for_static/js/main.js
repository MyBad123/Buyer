

for (let i of document.querySelectorAll('.item')) {
    i.onclick = (e) => {
        let refObject = e.target.closest('.item').querySelector('.item-ref').href;
        console.log(refObject);
        window.location.href = refObject;
    }
}

