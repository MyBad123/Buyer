// choice location for google
for (let i of document.querySelector('#google_btn').closest('.dropdown').querySelectorAll('li')) {
    i.addEventListener('click', () => {
        // get text from click element
        let text = i.innerText;

        // control value of this text
        if (text === 'Отключить геопозицию') {
            document.querySelector('#google_input').value = 'no';

            // else user choice 'Не искать в google'
            let controlElement = document.querySelector('#google_btn').innerHTML;
            if (controlElement === 'Не искать в google'){
                let elemYandex = document.querySelector('#yandex_btn').closest('.dropdown').querySelectorAll('li')[1];
                elemYandex.style.display = 'flex';
            }

            // change name for btn
            document.querySelector('#google_btn').innerHTML = text;
        }
        else if (text === 'Не искать в google') {
            document.querySelector('#google_input').value = 'no_search';

            // else user choice 'Не искать в google'
            let elemYandex = document.querySelector('#yandex_btn').closest('.dropdown').querySelectorAll('li')[1];
            elemYandex.style.display = 'none';

            // change name for btn
            document.querySelector('#google_btn').innerHTML = text;
        }
        else {
            document.querySelector('#google_input').value = text;

            // else user choice 'Не искать в google'
            let controlElement = document.querySelector('#google_btn').innerHTML;
            if (controlElement === 'Не искать в google'){
                let elemYandex = document.querySelector('#yandex_btn').closest('.dropdown').querySelectorAll('li')[1];
                elemYandex.style.display = 'flex';
            }

            // change name for btn
            document.querySelector('#google_btn').innerHTML = text;
        }
    });
}

// choice location for yandex
for (let i of document.querySelector('#yandex_btn').closest('.dropdown').querySelectorAll('li')) {
    i.addEventListener('click', () => {
        // get text from click element
        let text = i.innerText;

        if (text === 'Отключить геопозицию') {
            document.querySelector('#yandex_input').value = 'no';

            let controlElement = document.querySelector('#yandex_btn').innerHTML;
            if (controlElement === 'Не искать в yandex') {
                let elemGoogle = document.querySelector('#google_btn').closest('.dropdown').querySelectorAll('li')[1];
                elemGoogle.style.display = 'flex';
            }

            document.querySelector('#yandex_btn').innerHTML = text;
        }
        else if (text === 'Не искать в yandex') {
            document.querySelector('#yandex_input').value = 'no_search';

            let elemGoogle = document.querySelector('#google_btn').closest('.dropdown').querySelectorAll('li')[1];
            elemGoogle.style.display = 'none';

            // change name for btn
            document.querySelector('#yandex_btn').innerHTML = text;
        }
        else {
            document.querySelector('#yandex_input').value = text;

            // else user choice 'Не искать в google'
            let controlElement = document.querySelector('#yandex_btn').innerHTML;
            if (controlElement === 'Не искать в yandex') {
                let elemGoogle = document.querySelector('#google_btn').closest('.dropdown').querySelectorAll('li')[1];
                elemGoogle.style.display = 'flex';
            }

            document.querySelector('#yandex_btn').innerHTML = text;
        }
    });
}
