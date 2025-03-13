// document.addEventListener("DOMContentLoaded", function(){
//     async function loadLogin() {
//         await new Promise(resolve => setTimeout(resolve, 3000));
//         let response = await fetch('/login');
//         let html = await response.text();
//         document.getElementById('login-container').innerHTML = html;
//     }

//     loadLogin();
// });

function togglePasswordVisibility() {
    let passwordInput = document.getElementById("password");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let messages = document.querySelectorAll(".flash-message");
        messages.forEach(function (message) {
            message.style.display = "none";  // Hide after timeout
        });
    }, 5000);  // 5 seconds
});

