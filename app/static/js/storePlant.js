const currentUrl = window.location.href;
const urlParts = currentUrl.split('/');
const id = urlParts.pop();
const url = `/api/product/${id}`;

const plantName = document.getElementById('store-plant-name');
const sname = document.getElementById('store-plant-sname');
const plantImg = document.getElementById('store-plant-img');
const plantPrice = document.getElementById('store-plant-price');
const storeRedirect = document.querySelector('.store-plant-more-info');
const quantitySelect = document.querySelector('.quantity-width');
const cartQuantity = document.getElementById('cart-quantity');

storeRedirect.href = `../info/${id}`;

fetch(url)
  .then((response) => response.json())
  .then((data) => {
    plantName.textContent = data.name;
    sname.textContent = data.sname;
    plantImg.src = data.img;
    plantPrice.textContent = "CA$ " + data.price;

    // Retrieve the existing cart items from localStorage or create an empty array
    const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];

    // Calculate the total quantity from the cart items
    const totalQuantity = cartItems.reduce((total, item) => total + item.quantity, 0);

    // Update the cart quantity display
    cartQuantity.textContent = totalQuantity;
  })
  .catch((error) => console.error(error));

const addToCartButton = document.querySelector('.store-plant-btn');
addToCartButton.addEventListener('click', function () {
  // Retrieve the selected quantity from the dropdown
  const quantity = document.querySelector('.quantity-width').value;

  // Retrieve the existing cart items from localStorage or create an empty array
  const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];

  // Check if the plant is already in the cart
  const existingItemIndex = cartItems.findIndex((item) => item.plantName === plantName.textContent);

  if (existingItemIndex > -1) {
    // Plant already exists in the cart, update the quantity
    cartItems[existingItemIndex].quantity += parseInt(quantity);
  } else {
    // Plant doesn't exist in the cart, create a new item
    const newItem = {
      p_id: id,
      plantName: plantName.textContent,
      sname: sname.textContent,
      img: plantImg.src,
      quantity: parseInt(quantity),
      price: plantPrice.textContent,
    };
    cartItems.push(newItem);
  }

  // Update the cart quantity display
  const totalQuantity = cartItems.reduce((total, item) => total + item.quantity, 0);
  cartQuantity.textContent = totalQuantity;

  // Save the updated cart items to localStorage
  localStorage.setItem('cartItems', JSON.stringify(cartItems));

  // Log the contents of cartItems
  console.log(cartItems);
});
