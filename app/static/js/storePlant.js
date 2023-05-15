const currentUrl = window.location.href;
const urlParts = currentUrl.split('/');
const id = urlParts.pop();
const url =
    `/api/product/${id}`;

const plantName = document.getElementById('store-plant-name');
const sname = document.getElementById('store-plant-sname');
const img = document.getElementById('store-plant-img');
const price = document.getElementById('store-plant-price');
const storeRedirect = document.querySelector('.store-plant-more-info') 

storeRedirect.href = `info/${id}`;
fetch(url)
    .then((response) => response.json())
    .then((data) => {
        plantName.textContent = data.name
        sname.textContent = data.sname
        img.src = data.img
        price.textContent = "CA$ " + data.price
    })
    .catch((error) => console.error(error));


    