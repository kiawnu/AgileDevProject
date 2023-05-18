      // Retrieve the necessary elements
      const addToCartBtn = document.querySelector('.store-plant-btn');
      const cartQuantity = document.querySelector('#cart-quantity');
      const plantName = document.querySelector('#store-plant-name');
      const sname = document.querySelector('#store-plant-sname');
      const plantImg = document.querySelector('#store-plant-img');
      const plantPrice = document.querySelector('#store-plant-price');

      // Add click event listener to the "Add To Cart" button
      addToCartBtn.addEventListener('click', function() {
        // Retrieve the selected quantity from the dropdown
        const quantity = document.querySelector('.quantity-width').value;

        // Retrieve the existing cart items from localStorage or create an empty array
        const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];

        // Check if the plant is already in the cart
        const existingItemIndex = cartItems.findIndex(item => item.plantName === plantName.textContent);

        if (existingItemIndex > -1) {
          // Plant already exists in the cart, update the quantity
          cartItems[existingItemIndex].quantity += parseInt(quantity);
        } else {
          // Plant doesn't exist in the cart, create a new item
          const newItem = {
            plantName: plantName.textContent,
            sname: sname.textContent,
            img: plantImg.src,
            quantity: parseInt(quantity),
            price: plantPrice.textContent
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