const login = document.getElementById('login');
function clearLocalStorage() {
    localStorage.clear();
  }

login.addEventListener('click', clearLocalStorage)
