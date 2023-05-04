const createAccountButton = document.getElementById('create-account-btn');

const routeToCreateAccount = () => {
    event.preventDefault();
    window.location.href = '/createaccount';
};

createAccountButton.addEventListener('click', routeToCreateAccount);
