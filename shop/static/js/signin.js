window.onload = function() {
    document.getElementById("userForm").reset();
};

let btn = document.getElementById("subBtn");

function isValidPassword(password) {
    const specialCharRegex = /[!@#$%^&*(),.?":{}|<>]/;
    const uppercaseRegex = /[A-Z]/;
    const lowercaseRegex = /[a-z]/;
    const lengthRegex = /.{8,}/;

    return specialCharRegex.test(password) &&
        uppercaseRegex.test(password) &&
        lowercaseRegex.test(password) &&
        lengthRegex.test(password);
}

btn.addEventListener("click", (e) => {
    e.preventDefault();

    let userName = document.getElementById("user_name");
    let userNameValue = userName.value;
    let userNameFlag = false;

    let email = document.getElementById("email");
    let emailValue = email.value;
    let emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
    let emailFlag = false;

    let password = document.getElementById("password");
    let passwordValue = password.value;
    let passwordFlag = false;

    let address = document.getElementById("user_address");
    let addressValue = address.value;
    let addressFlag = false;

    if (userNameValue == "") {
        alert("Enter user name");
        userName.focus();
        return false;
    }
    else {
        userNameFlag = true;
    }

    if (emailValue == "" || emailPattern.test(emailValue) == false) {
        alert("Enter Valid Email Address");
        email.focus();
        return false;
    }
    else {
        emailFlag = true;
    }

    if (!isValidPassword(passwordValue)) {
        alert('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one special character.');
        return false;
    }
    else {
        passwordFlag = true;
    }

    if (addressValue == "") {
        alert("Enter Valid Address");
        address.focus();
        return false;
    }
    else {
        addressFlag = true;
    }

    if (userNameFlag && emailFlag && passwordFlag && addressFlag) {
        document.getElementById("userForm").submit();
    }
});