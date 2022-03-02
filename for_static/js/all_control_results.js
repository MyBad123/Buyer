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
        }
        else {
            e.target.closest(".item").classList.add("with-click");

            // add mail to form
            let wow = e.target.closest(".item").querySelector('td').innerHTML;
            
            document.querySelector(".modal-body").insertAdjacentHTML(
                'beforeBegin', 
                `<button type="button" class="btn btn-primary m-1">${ wow }</button>`
            )
        }
    }
}
