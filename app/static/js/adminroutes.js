// Buttons
const addProductButton = document.getElementById('addbtn');
const editProductButton = document.getElementById('updatebtn');
const delProductButton = document.getElementById('delbtn');

// Input Fields
const productID = document.getElementById('id');
const productName = document.getElementById('name');
const productSName = document.getElementById('sname');
const productPrice = document.getElementById('price');
const productQuant = document.getElementById('quantity');

// Add Product
const routeToAddProduct = () => {
  const dataObj = {
    name: productName.value,
    sname: productSName.value,
    price: parseFloat(productPrice.value),
    quantity: parseInt(productQuant.value)
  };
  console.log(dataObj);

  fetch("/admin/store/newproduct", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dataObj)
  })
    .then(data => console.log(data))
    .catch(err => console.log(err));
};

addProductButton.addEventListener('click', routeToAddProduct);

// Delete Product
const routeToDelProduct = () => {
  fetch(`/admin/store/${productID.value}`, {
    method: 'DELETE',
  })
  .then(response => {
    if (response.status === 404) {
      alert("That item does not exist!")
    } else if (response.status === 400) {
      alert("Invalid attributes!")
    }
  })
    .then(data => console.log(data))
    .catch(err => console.log(err));
};

delProductButton.addEventListener('click', routeToDelProduct);

// Modify Product
const routeToEditProduct = () => {
  event.preventDefault();
  const dataObj = {
    id: productID.value,
    name: productName.value,
    price: parseFloat(productPrice.value),
    quantity: parseInt(productQuant.value)
  };
  console.log(dataObj);

  fetch(`/admin/store/${productID.value}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json' // Fixed typo in header name
    },
    body: JSON.stringify(dataObj)
  })
  .then(response => {
    if (response.status === 404) {
      alert("That item does not exist!")
    }
  })
    .then(data => console.log(data))
    .catch(err => console.log(err));
};

editProductButton.addEventListener('click', routeToEditProduct);
