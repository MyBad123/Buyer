

for (let i of document.querySelectorAll('.item')) {
    i.onmouseover = (e) => {
        e.target.closest(".item").classList.add("table-primary");
    }
    i.onmouseout = (e) => {
        e.target.closest(".item").classList.remove("table-primary");
    }
    
    i.onclick = (e) => {
        let refObject = e.target.closest('.item').querySelector('.item-ref').href;
        console.log(refObject);
        window.location.href = refObject;
    }
}

