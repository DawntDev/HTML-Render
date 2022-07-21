let i = 4;

window.onload = function() {
    setTimeout(() => {
        window.location.href = '/';
    }, (i + 1) * 1000);

    setInterval(() => {
        let message = document.getElementById("message");
        message.innerText = `The page you are looking for does not exist. Returning to the start in ${i} seconds...`;
        i --;
    }, 1000);
};