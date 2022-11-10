let btnAdd = document.querySelector('button');
let table = document.querySelector('table');

let nameInput = document.querySelector('#name');
let surNameInput = document.querySelector('#surname');
let postCodeInput = document.querySelector('#postcode');
let streetInput = document.querySelector('#street');
let houseNumberInput = document.querySelector('#housenumber');
let teacherInput = document.querySelector('#teacher');

btnAdd.addEventListener('click', () => {
    let name = nameInput.value;
    let surname = surNameInput.value;
    let postcode = postCodeInput.value;
    let street = streetInput.value;
    let housenumber = houseNumberInput.value;
    let teacher = teacherInput.value;

    let template = `
                <tr>
                    <td>${name}</td>
                    <td>${surname}</td>
                    <td>${postcode}</td>
                    <td>${street}</td>
                    <td>${housenumber}</td>
                    <td>${teacher}</td>
                </tr>`;
    
    table.innerHTML += template 
});

// Ende von der Schülertabelle