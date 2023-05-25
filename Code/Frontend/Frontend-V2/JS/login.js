function login() {
    closeAuthPopup()
    var userName = document.getElementById("usernameField").value;
    var password = document.getElementById("passwordField").value;
    var url = "/";
	console.log(url)
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            console.log(xhr.status);
            console.log(xhr.responseText);
            var j = JSON.parse(xhr.responseText);
            if(xhr.status==200){
                window.location.href ="?token="+j.token;
            }
            else{
                document.getElementById("popupWrongUserOrPassword").classList.add("errorPopupAnimate")
            }
        }
    };
    var data = '{"username":"' + encodeURIComponent(userName) + '","password":"' + encodeURIComponent(password) + '"}';
    xhr.send(data);
};

function closeAuthPopup() {
    document.getElementById("popupWrongUserOrPassword").classList.remove("errorPopupAnimate")
}
