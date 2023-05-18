table = document.querySelector('.display tbody');
nameform = document.querySelector('.nameinp');
snameform = document.querySelector('.snameinp');
priceform = document.querySelector('.priceinp');
quantform = document.querySelector('.quantityinp');
table.addEventListener("click", dispitem);
nameform.value = "";
snameform.value = "";
priceform.value = "";
quantform.value = "";

function dispitem(i){
    rows = table.outerText.split('\n');
    attributes = rows[0].split('\t');

    const cell = i.target.closest('td');
    if (!cell){
        return;
    }
    const row = cell.parentElement;
    items = rows[row.rowIndex-1].split('\t')
    console.log(rows[row.rowIndex-1].split('\t'));

    nameform.value = items[2];
    snameform.value = items[3];
    priceform.value = items[4];
    quantform.value = items[5];
}

