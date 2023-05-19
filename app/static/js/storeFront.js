const url = "/api/products";
const searchContainer = document.querySelector("#searchContainer");
const plantList = document.querySelector("#display-block");
const plantSearch = document.getElementById("searchBox");
const cartQuantity = document.getElementById("cart-quantity");

fetch(url)
  .then((response) => response.json())
  .then((items) => {
    data = items;
    displayItems(data);
  })
  .catch((error) => console.error(error));

let data = [];

function displayItems(items) {
  plantList.innerHTML = "";
  items.forEach((species) => {
    const li = document.createElement("li");
    const a = document.createElement("a");
    const img = document.createElement("img");
    const h2 = document.createElement("h2");
    const h3 = document.createElement("h3");
    const h4 = document.createElement("h4");

    li.setAttribute("class", "species");

    a.href = `/store/${species.id}`;
    img.src = species.img;
    h2.textContent = species.name;
    h3.textContent = species.sname;
    h4.textContent = "CA$ " + species.price;

    a.appendChild(img);
    a.appendChild(h2);
    a.appendChild(h3);
    a.appendChild(h4);
    li.appendChild(a);
    plantList.appendChild(li);
  });

  updateCartQuantity();
}

function updateCartQuantity() {
  const storedQuantity = localStorage.getItem('cartQuantity');
  if (storedQuantity) {
    cartQuantity.textContent = storedQuantity;
  } else {
    const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
    const totalQuantity = cartItems.reduce((total, item) => total + item.quantity, 0);
    cartQuantity.textContent = totalQuantity;
  }
}

function sortItems() {
  let selectedValue = document.querySelector("#sortBy").value;
  let sortedItems = [];
  if (selectedValue === "-") {
    fetch(url)
      .then((response) => response.json())
      .then((items) => {
        data = items;
        displayItems(data);
      })
      .catch((error) => console.error(error));
  } else {
    if (selectedValue === "lowToHigh") {
      sortedItems = data.sort((a, b) => a.price - b.price);
    } else if (selectedValue === "highToLow") {
      sortedItems = data.sort((a, b) => b.price - a.price);
    }
    displayItems(sortedItems);
  }
}

function searchItems() {
  for (item of plantList.getElementsByTagName("li")) {
    if (
      item.innerHTML.includes(plantSearch.value) ||
      item.innerHTML.toUpperCase().includes(plantSearch.value.toUpperCase())
    ) {
      item.removeAttribute("class", "hidden");
    } else {
      item.setAttribute("class", "hidden");
    }
  }
}

plantSearch.addEventListener("input", searchItems);
document.querySelector("#sortBy").addEventListener("change", sortItems);

updateCartQuantity();
