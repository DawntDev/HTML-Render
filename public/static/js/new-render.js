// Handle type of render
let options = Array.from(document.querySelectorAll("li.element > button"));
let forms = Array.from(document.getElementsByClassName("form"));

options.forEach(opt => {
    opt.addEventListener("click", () => {
        if (options.indexOf(opt) === 0) {
            opt.parentElement.classList.add("active");
            options[1].parentElement.classList.remove("active");
            forms[1].classList.add("hidden");
            forms[0].classList.remove("hidden");
        } else {
            opt.parentElement.classList.add("active");
            options[0].parentElement.classList.remove("active");
            forms[0].classList.add("hidden");
            forms[1].classList.remove("hidden");
        }
    });
});

// Handle form submit
const clearForm = data => Object.entries(data).forEach(([key, value]) => Boolean(value) === false && delete data[key]);
function read(...files) {
    let reads = [];
    let reader = new FileReader();
    reader.onload = e => reads.push(e.target.result);
    
    files.forEach(f => f !== undefined && reader.readAsText(f));
    console.log(reads);
    return reads;
} ;

document.getElementById("render").addEventListener("submit", (e) => {
    e.preventDefault();
    let data = {
        html: document.getElementById("html").files[0],
        css: document.getElementById("css").files[0],
        js: document.getElementById("js").files[0],
        selector: document.getElementById("selector").value,
        format: document.getElementById("format").value,
        size: document.getElementById("size").value !== "" ? document.getElementById("size").value.split("x") : null,
        timeout: document.getElementById("timeout").value
    }

    clearForm(data);
    
    let {html, css, js} = data;
    console.log(read(html, css, js))
});

document.getElementById("urlToImage").addEventListener("submit", (e) => {
    e.preventDefault();
    let data = {
        url: document.getElementById("url").value,
        selector: document.getElementById("selector").value,
        format: document.getElementById("format").value,
        size: document.getElementById("size").value !== "" ? document.getElementById("size").value.split("x") : null,
        timeout: document.getElementById("timeout").value,
    }

    clearForm(data);
    console.log(data);
    fetch("/api/v1/urlToImage", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
        }
    ).then(res => {
        if (res.status === 200) {
            window.location.href = res.url;
        }
    });
});