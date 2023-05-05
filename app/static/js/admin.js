const loginButton = document.getElementById('submit');
const username = document.getElementById('username');
const password = document.getElementById('password');

const login = () => {
    event.preventDefault();
    let dataArray = []
    let dataObj = { username: '', password: '' }
    dataObj.username = username.value
    dataObj.password = password.value
    console.log(dataObj)
    fetch('/admin', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataObj)
    })
        .then(response => {
        if (response.status == 200) {
            window.location.href = '/admin/store'
        }//else{window.location.href = '/admin'}
        })
        .then(data => console.log(data))
        .catch(error => console.error(error));
};

loginButton.addEventListener('click', login);