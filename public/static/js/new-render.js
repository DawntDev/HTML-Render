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
const clearForm = data => Object.entries(data).forEach(([key, value]) => (Boolean(value) === false || value < 1) && delete data[key]);
const extractGroup = (text, regex) => [...text.matchAll(regex)].map(match => match[1]).join("\n");
function read(...files) {
    let reads = [];
    files.forEach(file => {
        reads.push(new Promise((resolve, reject) => {
            let reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = () => reject(reader.error);
            file ? reader.readAsText(file) : resolve(null);
        }));
    });
    return Promise.all(reads);
};

const loader = {
    show: () => {
        let container = document.createElement("div");
        container.classList.add("loader");
        container.innerHTML = `
            <div class="spinner">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
            <div class="text">
                <span>Rendering...</span>
            </div>
        `;

        document.body.appendChild(container);
    },
    hide: () => {
        let container = document.querySelector(".loader");
        container.remove();
    },
    alert: (message, subtext = False) => {
        let container = document.createElement("div");
        container.classList.add("alert");
        container.innerHTML = `
            <div class="message">
                <span class="title">
                    ${message}
                    <div></div>
                </span>
                ${subtext ? `<span class="subtext">${subtext}</span>` : ""}
                <button id="close">close</button>
            </div>
        `;
        container.querySelector("#close").addEventListener("click", () => container.remove());
        document.body.appendChild(container);
    }
};

document.getElementById("render").addEventListener("submit", (e) => {
    e.preventDefault();
    let data = {
        html: document.getElementById("html").files[0],
        css: document.getElementById("css").files[0],
        js: document.getElementById("js").files[0],
        selector: document.getElementById("render-selector").value,
        format: document.getElementById("render-format").value,
        size: document.getElementById("render-size").value !== "" ? document.getElementById("render-size").value.split("x") : null,
        timeout: Number(document.getElementById("render-timeout").value) + (.1 * [10 ** -5])
    }
    clearForm(data);

    const { html, css, js, ...args } = data;
    read(html, css, js).then(([html, css, js]) => {
        let body = {
            elements: html,
            css: css,
            js: js,
            ...args
        }
        clearForm(body);

        loader.show();
        fetch("api/v1/render", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        }).then(res => {
            if (res.status === 200) {
                loader.hide();
                window.location.href = res.url;
            } else {
                loader.hide();
                res.text().then(text => {
                    let regex = /li>([\s\S]*?)<\/li/g;
                    text = text.replace(/\n*/gm, "");
                    loader.alert(`Error: ${res.status}`, extractGroup(text, regex));
                });
            };
        }).catch(err => {
            loader.hide();
            loader.alert(err.message);
        });
    })
});

document.getElementById("urlToImage").addEventListener("submit", (e) => {
    e.preventDefault();
    let data = {
        url: document.getElementById("url").value,
        selector: document.getElementById("urlToImage-selector").value,
        format: document.getElementById("urlToImage-format").value,
        size: document.getElementById("urlToImage-size").value !== "" ? document.getElementById("urlToImage-gsize").value.split("x") : null,
        timeout: Number(document.getElementById("urlToImage-timeout").value) + (.1 * [10 ** -5]),
    }
    clearForm(data);

    loader.show();
    fetch("/api/v1/urlToImage", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }
    ).then(res => {
        if (res.status === 200) {
            loader.hide();
            window.location.href = res.url;
        } else {
            loader.hide();
            res.text().then(text => {
                let regex = /li>([\s\S]*?)<\/li/g;
                text = text.replace(/\n*/gm, "");
                loader.alert(`Error: ${res.status}`, extractGroup(text, regex));
            });
        };
    }).catch(err => {
        loader.hide();
        loader.alert(err.message);
    });
});