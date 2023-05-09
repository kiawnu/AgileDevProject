const currentUrl = window.location.href;
const urlParts = currentUrl.split('/');
const id = urlParts.pop();
const url =
    `/api/product/${id}`;

const plantName = document.getElementById('name');
const sname = document.getElementById('sname');
const img = document.getElementById('img');
const price = document.getElementById('price');


fetch(url)
    .then((response) => response.json())
    .then((data) => {
        plantName.textContent = data.name
        sname.textContent = data.sname
        img.src = data.img
        price.textContent = data.price
    })
    .catch((error) => console.error(error));