// work with table
for (let i of document.querySelectorAll(".item")) {
    i.onmouseover = (e) => {
        e.target.closest(".item").classList.add("table-primary");
    }
    i.onmouseout = (e) => {
        if (!(e.target.closest(".item").classList.contains('with-click'))) {
            e.target.closest(".item").classList.remove("table-primary");
        }
    }
    i.onclick = (e) => {
        if (e.target.closest(".item").classList.contains("with-click")) {
            e.target.closest(".item").classList.remove("with-click");
            
            // remove amil from form 
            let wow = e.target.closest(".item").querySelector('td').innerHTML;

            let index = 0;
            for (let j of document.querySelector('.modal-body').querySelectorAll('button')) {
                if ((j.innerHTML === wow) && (index === 0)) {
                    document.querySelector('.modal-body').removeChild(j);
                    index += 1;
                }
            }
        }
        else {
            e.target.closest(".item").classList.add("with-click");

            // add mail to form
            let wow = e.target.closest(".item").querySelector('td').innerHTML;
            
            document.querySelector(".modal-body").insertAdjacentHTML(
                'afterBegin', 
                `<button type="button" class="btn btn-primary m-1">${ wow }</button>`
            )
        }
    }
}
