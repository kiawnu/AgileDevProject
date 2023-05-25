let data = []
let selectedItem = ''
let dataTable = null

function loadTable() {
  fetch('/api/products')
    .then((response) => response.json())
    .then((items) => {
      data = items;

      if (dataTable !== null) {
        dataTable.destroy();
      }

      dataTable = $('#myTable').DataTable({
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
}

$(document).ready(function () {
  loadTable();
});

function refreshTable() {
  loadTable();
}


table = document.querySelector('.display tbody');
nameform = document.querySelector('.nameinp');
snameform = document.querySelector('.scinameinp');
priceform = document.querySelector('.priceinp');
quantform = document.querySelector('.quantityinp');
imgform = document.querySelector('.imginp');
table.addEventListener("click", dispitem);

addBtn = document.querySelector('.addbtn');
deleteBtn = document.querySelector('.delbtn');
updateBtn = document.querySelector('.updatebtn');

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

  for (item of data) {
    if (item.id === Number(id)) {
      selectedItem = item;
      imgform.value = item.img
      nameform.value = item.name
      snameform.value = item.sname
      priceform.value = item.price
      quantform.value = item.quantity
    }
  }
}

const addItem = () => {
  let isDuplicate = false;

  for (const item of data) {
    if (imgform.value === item.img || nameform.value === item.name || snameform.value === item.sname) {
      isDuplicate = true;
      break;
    }
  }

  if (isDuplicate) {
    alert("Item Already in database. Please check inputs!");
    return;
  }

  const newItem = {
    img: imgform.value,
    name: nameform.value,
    sname: snameform.value,
    price: priceform.value,
    quantity: quantform.value
  };
  fetch('/admin/store/newproduct', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(newItem)
  })
    .then((response) => response.text())
    .then((data) => {
      alert(data);
    });
    window.location.href = '/admin/store'
};

const deleteItem = () => {
  fetch(`/admin/store/${selectedItem.id}`, {
    method: 'DELETE',
  })
    .then((response) => response.text())
    .then((data) => {
      alert(data);
    });
    window.location.href = '/admin/store'
}

const updateItem = () => {
  const item = {
    img: imgform.value,
    name: nameform.value,
    sname: snameform.value,
    price: priceform.value,
    quantity: quantform.value
  };
  fetch(`/admin/store/${selectedItem.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(item)
  })
    .then((response) => response.text())
    .then((data) => {
      alert(data);
    });
    window.location.href = '/admin/store'
}
addBtn.addEventListener("click", addItem);
deleteBtn.addEventListener("click", deleteItem);
updateBtn.addEventListener("click", updateItem);
