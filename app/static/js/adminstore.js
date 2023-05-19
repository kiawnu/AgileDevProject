let data = []
$(document).ready(function () {
  fetch('/api/products')
    .then((response) => response.json())
    .then((items) => {
      items.forEach((species) => { data.push(species) })

      $('#myTable').DataTable({
        data: data,
        columns: [
          { data: 'id' },
          {
            data: 'img', render: function (data) {
              return '<img src="' + data + '" width="100" height="100">';
            }
          }, { data: 'sname' },
          { data: 'name' },
          { data: 'price' },
          { data: 'quantity' },
        ]
      });
    })
    .catch((error) => console.error(error));

});


table = document.querySelector('.display tbody');
nameform = document.querySelector('.nameinp');
snameform = document.querySelector('.snameinp');
priceform = document.querySelector('.priceinp');
quantform = document.querySelector('.quantityinp');
imgform = document.querySelector('.imginp');
table.addEventListener("click", dispitem);
imgform.value = "";
nameform.value = "";
snameform.value = "";
priceform.value = "";
quantform.value = "";

function dispitem(i) {
  rows = table.outerText.split('\n');
  attributes = rows[0].split('\t');

  const cell = i.target.closest('td');
  if (!cell) {
    return;
  }
  const row = cell.parentElement;
  items = rows[row.rowIndex - 1].split('\t')
  console.log(rows[row.rowIndex - 1].split('\t'));

  for (item of data){
    if (item.name === items[3]){
      imgform.value = item.img
    }
  }
  nameform.value = items[2];
  snameform.value = items[3];
  priceform.value = items[4];
  quantform.value = items[5];
}
