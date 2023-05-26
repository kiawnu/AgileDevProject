const updateLocalStorage = () => {
    fetch("/loginstatus")
    .then((response) => {
        if (response.status === 200) {
            fetch("/orders")
            .then((orders) => {
                orders.text()
                .then((data) => {
                    order = JSON.parse(data);
                    let cartItems = [];
                    for (const product of order["products"]) {
                        cartItems.push(product);
                    }
                    localStorage.cartItems = JSON.stringify(cartItems);
                })
            })
        }
    })
}

updateLocalStorage();