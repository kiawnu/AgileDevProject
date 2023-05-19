// const addProductButton = document.getElementById('addbtn');
// const editProductButton = document.getElementById('updatebtn');
// const delProductButton = document.getElementById('delbtn');

// const productID = document.getElementById('product-id');
// const productName = document.getElementById('product-name');
// const productPrice = document.getElementById('product-price');
// const prodcutQuant = document.getElementById('product-quant');

// //add
// const routeToAddProduct = () => {
//     event.preventDefault();
//     let dataObj = {'name':'', 'price':0.0, 'quantity':0};
//     dataObj.name = productName.value;
//     dataObj.price = productPrice.value;
//     dataObj.quantity = prodcutQuant.value;
//     console.log(dataObj);
// };

// fetch("/admin/store/newproduct", {
//     method:'POST',
//     headers:{
//         'Content-Headers':'application/json'
//     },
//     body:JSON.stringify(dataObj)
// })
// .then(response => {
//     if (response.status == 200){
//         window.location.href = '/admin/store';
//     } else {
//         window.location.href = '/admin/store';
//     }
// })
// .then(data => console.log(data))
// .catch(err => console.log(err));

// addProductButton.addEventListener('click', routeToAddProduct);

// //remove
// const routeToDelProduct = () => {
    
// };

// fetch(`/admin/store/${productID.value}`, {
//     method:'DELETE',
// })
// .then(response => {
//     if (response.status == 200){
//         window.location.href = '/admin/store';
//     } else {
//         window.location.href = `/admin/store`;
//     }
// })
// .then(data => console.log(data))
// .catch(err => console.log(err));

// delProductButton.addEventListener('click', routeToDelProduct);

// //update
// const routeToEditProduct = () => {
//     event.preventDefault();
//     let dataObj = {'id':0, 'name':'', 'price':0.0, 'quantity':0};
//     dataObj.id = productID.value;
//     dataObj.name = productName.value;
//     dataObj.price = productPrice.value;
//     dataObj.quantity = prodcutQuant.value;
//     console.log(dataObj);
// };

// fetch(`/admin/store/${productID.value}`, {
//     method:'PUT',
//     headers:{
//         'Content-Headers':'application/json'
//     },
//     body:JSON.stringify(dataObj)
// })
// .then(response => {
//     if (response.status == 200){
//         window.location.href = '/admin/store';
//     } else {
//         window.location.href = `/admin/store`;
//     }
// })
// .then(data => console.log(data))
// .catch(err => console.log(err));

// editProductButton.addEventListener('click', routeToEditProduct);

const addProductButton = document.getElementById('addbtn');
const editProductButton = document.getElementById('updatebtn');
const delProductButton = document.getElementById('delbtn');

const productID = document.getElementById('id');
const productName = document.getElementById('name');
const productSName = document.getElementById('sname');
const productPrice = document.getElementById('price');
const productQuant = document.getElementById('quantity');

// Function to handle adding a product
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

// Function to handle deleting a product
const routeToDelProduct = () => {
  fetch(`/admin/store/${productID.value}`, {
    method: 'DELETE',
  })
    .then(data => console.log(data))
    .catch(err => console.log(err));
};

delProductButton.addEventListener('click', routeToDelProduct);

// Function to handle updating a product
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
    .then(data => console.log(data))
    .catch(err => console.log(err));
};

editProductButton.addEventListener('click', routeToEditProduct);
