// for table
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

// elem in arr or no
let inArr = (elem, arr) => {
    let index = 0;
    for (let i of arr) {
        if (elem == i) {
            index += 1;
        }
    }

    if (index === 0) {
        return false
    }
    else {
        return true
    }

}

// for status in real time
let periodicApiFunc = async () => {
    console.log('www')

    // make request for getting api
    let request = await fetch('/user-page-api/');
    let response = await request.json();


    // get all if for control
    let arrayId = [];
    for (let i of response.status) {
        arrayId.push(i.id);
    }

    // update status in table
    for (let i of document.querySelectorAll('.item-ref')) {
        // get id of table object
        let forId = i.href.split('/').length;
        let objId = i.href.split('/')[forId -2];

        // update
        if (inArr(objId, arrayId)) {
            for (let j of response.status) {
                if (j.id == objId) {
                    i.closest('.item').querySelectorAll('td')[4].innerText = j.status;
                }
            }
        }
    }
}
setInterval(periodicApiFunc, 5000);

