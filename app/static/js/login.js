const createAccountButton = document.getElementById('create-account-btn');
const loginButton = document.getElementById('login-btn');
const username = document.getElementById('username');
const password = document.getElementById('password');

const routeToCreateAccount = () => {
    event.preventDefault();
    window.location.href = '/createaccount';
};

const login = () => {
    event.preventDefault();
    let dataArray = []
    let dataObj = { username: '', password: '' }
    dataObj.username = username.value
    dataObj.password = password.value
    localStorage.clear();
    console.log(dataObj)
    fetch('/login', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataObj)
    })
        .then(response => {
        if (response.status == 200) {
            window.location.href = '/'
        }else{window.location.href = '/login'}
        })
        .then(data => console.log(data))
        .catch(error => console.error(error));
};
const getLocalStorage = () => {
    
}

loginButton.addEventListener('click', login);

createAccountButton.addEventListener('click', routeToCreateAccount);
