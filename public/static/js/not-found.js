// Return to the start page in n seconds
let n = 4;

window.onload = function() {
    setTimeout(() => {
        window.location.href = '/';
    }, (n + 1) * 1000);

    setInterval(() => {
        let message = document.getElementById("message");
        message.innerText = `The page you are looking for does not exist. Returning to the start in ${n} seconds...`;
        n --;
    }, 1000);
};