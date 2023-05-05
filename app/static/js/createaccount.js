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