var count = 3;
var timer = setInterval(function() {
  count--;
  document.getElementById("timer").innerHTML = "Redirecting in " + count + " seconds...";
  if (count === 0) {
    clearInterval(timer);
    window.location.href = "/login";
  }
}, 1000);


