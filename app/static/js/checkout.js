// Retrieve the shopping cart items from localStorage
const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];

// Get the checkout item list element
const checkoutItemList = document.getElementById('checkout-item-list');

// Get the cart quantity element
const cartQuantity = document.getElementById('cart-quantity');

let totalSubtotal = 0;

// Function to update the total quantity
function updateSubTotalQuantity() {
  const totalQuantity = cartItems.reduce((total, item) => total + item.quantity, 0);
  cartQuantity.textContent = totalQuantity;
}

// Function to update the subtotal, total amount in the shopping cart and order summary
function updateSubTotal() {
  const subtotal = cartItems.reduce((total, item) => {
    const price = parseFloat(item.price.substring(4));
    return total + price * item.quantity;
  }, 0);
  
  const taxPercentage = 5; // Assuming 5% GST
  const tax = (subtotal * taxPercentage) / 100;
  const total = subtotal + tax;

  const taxAmount = document.getElementById('tax-amount');
  const totalAmount = document.getElementById('total-amount');

  taxAmount.textContent = `CA$${tax.toFixed(2)}`;
  totalAmount.textContent = `CA$${total.toFixed(2)}`;
  document.getElementById('subtotal-amount').textContent = `CA$${subtotal.toFixed(2)}`;
}



// Function to update the quantity of an item in the shopping cart
function updateQuantity(index, quantity) {
  cartItems[index].quantity = quantity;
  localStorage.setItem('cartItems', JSON.stringify(cartItems));
  updateSubTotalQuantity();
  updateSubTotal();
  renderCheckoutItems();
}

// Function to remove an item from the shopping cart
function removeItem(index) {
  cartItems.splice(index, 1);
  localStorage.setItem('cartItems', JSON.stringify(cartItems));
  renderCheckoutItems();
  updateSubTotalQuantity();
  updateSubTotal();
}

// Function to render the checkout items in the shopping cart
function renderCheckoutItems() {
  checkoutItemList.innerHTML = '';

  const tableBody = document.createElement('tbody');
  const tableHeadings = document.createElement('thead');

  // Create table headings row
  const tableHeadingsRow = document.createElement('tr');
  tableHeadingsRow.innerHTML = `
    <th>#</th>
    <th>Image</th>
    <th>Plant Name</th>
    <th>Scentific Name</th>
    <th>Quantity</th>
    <th>Price(CA$)</th>
    <th>Subtotal</th>
    <th></th>
    
  `;
  tableHeadings.appendChild(tableHeadingsRow);

  cartItems.forEach((item, index) => {
    const tableRow = document.createElement('tr');
    tableRow.innerHTML = `
      <td>${index + 1}</td>
      <td>
        <img src="${item.img}" alt="Plant Image" class="checkout-plant-image">
      </td>
      <td>${item.plantName}</td>
      <td>${item.sname}</td>
      <td>
        <input type="number" class="quantity-input" value="${item.quantity}" min="1">
      </td>
      <td>${parseFloat(item.price.substring(4))}</td>
      <td>${(parseFloat(item.price.substring(4)) * item.quantity).toFixed(2)}</td>
      <td>
        <button class="delete-button">Delete</button>
      </td>
    `;

    // Add event listener for the quantity input
    const quantityInput = tableRow.querySelector('.quantity-input');
    quantityInput.addEventListener('change', (event) => {
      const quantity = parseInt(event.target.value);
      updateQuantity(index, quantity);
    });

    // Add event listener for the delete button
    const deleteButton = tableRow.querySelector('.delete-button');
    deleteButton.addEventListener('click', () => {
      removeItem(index);
    });

    tableBody.appendChild(tableRow);

    totalSubtotal += parseFloat(item.price.substring(4)) * item.quantity; // Calculate the total subtotal
  });

  const subtotalRow = document.createElement('tr');
  subtotalRow.innerHTML = `
    <td class="subtotal-line" colspan="6">Subtotal</td>
    <td class="subtotal-cell" colspan="2">CA$ ${totalSubtotal.toFixed(2)}</td>
  `;
  tableBody.appendChild(subtotalRow);

  const table = document.createElement('table');
  table.appendChild(tableHeadings);
  table.appendChild(tableBody);

  checkoutItemList.appendChild(table);
  updateSubTotalQuantity();
  updateSubTotal();
}


// Initial rendering of the checkout items
renderCheckoutItems();
updateSubTotalQuantity();
updateSubTotal();
