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
snameform = document.querySelector('.scinameinp');
priceform = document.querySelector('.priceinp');
quantform = document.querySelector('.quantityinp');
imgform = document.querySelector('.imginp');
table.addEventListener("click", dispitem);

function dispitem(i) {
  rows = table.outerText.split('\n');
  attributes = rows[0].split('\t');

  const cell = i.target.closest('td');
  if (!cell) {
    return;
  }
  const row = cell.parentElement;
  items = rows[row.rowIndex - 1].split('\t')
  id = items[0]

  for (item of data){
    if (item.id === Number(id)){
      imgform.value = item.img
      nameform.value = item.name
      console.log(item)
      snameform.value = item.sname
      priceform.value = item.price
      quantform.value = item.quantity
    }
  }
}
