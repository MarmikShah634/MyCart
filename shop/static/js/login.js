function redirectToSignIn() {
    // Show the overlay
    document.getElementById('overlay').style.display = 'flex';

    document.body.classList.add('disable-interaction');

    // Redirect after 3 seconds
    setTimeout(function () {
        window.location.href = "/shop/signin";  // Adjust the URL name as needed
    }, 3000);
}