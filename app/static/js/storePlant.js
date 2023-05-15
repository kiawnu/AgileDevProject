const currentUrl = window.location.href;
const urlParts = currentUrl.split('/');
const id = urlParts.pop();
const url =
    `/api/store/${id}`;

const plantName = document.getElementById('store-plant-name');
const sname = document.getElementById('store-plant-sname');
const img = document.getElementById('store-plant-img');
const price = document.getElementById('store-plant-price');
const storeRedirect = document.querySelector('.store-plant-more-info') 

const quantitySelect = document.querySelector('.quantity-width');
const cartImage = document.getElementById('store-plant-shopCart-img');
const cartQuantityElement = document.getElementById('cart-quantity')

storeRedirect.href = `../info/${id}`;
fetch(url)
    .then((response) => response.json())
    .then((data) => {
        plantName.textContent = data.name
        sname.textContent = data.sname
        img.src = data.img
        price.textContent = "CA$ " + data.price
    })
    .catch((error) => console.error(error));


function addToCart(event) {
    event.preventDefault();
    
    const selectedQuantity = quantitySelect.value;
    cartImage.alt = 'shopping_cart (' + selectedQuantity + ')';
    cartQuantityElement.innerText = selectedQuantity; // Update quantity in the cart-quantity span element
    quantitySelect.value = 1;
    }
    
    const addToCartButton = document.querySelector('.store-plant-btn');
    addToCartButton.addEventListener('click', addToCart);
    