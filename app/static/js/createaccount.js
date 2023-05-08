const createAccountButton = document.getElementById('create-account-btn');
const username = document.getElementById('username');
const password = document.getElementById('password');

const routeToCreateAccount = () => {
  event.preventDefault();
  let dataArray = []
  let dataObj = { username: '', password: '' }
  dataObj.username = username.value
  dataObj.password = password.value
  console.log(dataObj)
  fetch('/createaccount', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dataObj)
  })
    .then(response => {
      if (response.status == 200) {
        window.location.href = '/'
      }else{window.location.href = '/createaccount'}
    })
    .then(data => console.log(data))
    .catch(error => console.error(error));
};

createAccountButton.addEventListener('click', routeToCreateAccount);


const routeToCreateAccount = () => {
  event.preventDefault();
  let dataArray = []
  let dataObj = { name: '', price: '', quanitiy: }
  dataObj.username = username.value
  dataObj.password = password.value
  console.log(dataObj)
  fetch('/admin/store', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dataObj) //{'name': 'apple tree', 'price': 1, 'quantity': 1}
  })
    .then(response => {
      if (response.status == 200) {
        window.location.href = '/admin/store'
      }else{window.location.href = '/admin/store'}
    })
    .then(data => console.log(data))
    .catch(error => console.error(error));
};