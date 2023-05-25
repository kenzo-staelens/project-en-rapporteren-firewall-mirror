var logout = document.getElementById("logout");
var toLogin = document.getElementById("toLogin");
var login = document.getElementById("login");
var toDashboard = document.getElementById("toDashboard");
var toTraffic = document.getElementById("toTraffic");
var toSettings = document.getElementById("toSettings");
var toThreats = document.getElementById("threats");

if (logout) {
  logout.addEventListener("click", function () {
    window.location.replace("logout.html");
  });
}

if (toLogin)
  toLogin.addEventListener("click", function () {
    window.location.replace("login.html");
  });

if (login)
  login.addEventListener("click", function () {
    window.location.replace("home.html");
  });

if (toDashboard)
  toDashboard.addEventListener("click", function () {
    window.location.replace("dashboard.html");
  });

if (threats)
  threats.addEventListener("click", function () {
    window.location.replace("dashboard.html");
  });

if (toTraffic)
  toTraffic.addEventListener("click", function () {
    window.location.replace("traffic.html");
  });

if (toSettings)
  toSettings.addEventListener("click", function () {
    window.location.replace("settings.html");
  });
