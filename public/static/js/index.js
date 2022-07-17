const imgs = [
    "static/img/bongo-cat-codes-2jamming.webp",
    "static/img/computer-store-landing-page.webp",
    "static/img/generative-kong-summit-patterns.webp",
    "static/img/responsive-social-platform-ui.webp"
];


// Render the dynamic images
window.onload = function () {
    const container = document.querySelector("div#example")
    const len = imgs.length - 1;

    let i = 1;
    setInterval(() => {
        let src = imgs[i];
        container.style.backgroundImage = `url(http://127.0.0.1:5000/${src})`;
        i = (i < len) ? i + 1 : 0;
    }, 5000);
};

// Options
let optionsButtons = Array.from(document.querySelector("div#document").childNodes).filter(node => node.type === "button");

let elements = document.querySelectorAll("div.option");
let lastActive = document.querySelector("div#document > button.active");

optionsButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        if (!btn.classList.contains("active")) {
            btn.classList.add("active");
            lastActive.classList.remove("active");

            elements[optionsButtons.indexOf(btn)].style = "display: block";
            elements[optionsButtons.indexOf(lastActive)].style = "display: none";

            lastActive = btn;
        };
    });
});

// Requests
let requestButtons = Array.from(document.querySelector("div#btn-request").childNodes);

let render = document.querySelector("table#request-render");
let urlToImage = document.querySelector("table#request-urlToImage");

requestButtons.forEach(btn => {
    if (btn.type === "button") {
        btn.addEventListener("click", () => {
            if (!btn.classList.contains("active")) {
                btn.classList.add("active");

                if (requestButtons.indexOf(btn) === 1) {
                    requestButtons[3].classList.remove("active");
                    render.style = "display: table";
                    urlToImage.style = "display: none";
                } else {
                    requestButtons[1].classList.remove("active");
                    render.style = "display: none";
                    urlToImage.style = "display: table";
                };
            };
        });
    };
});

// TSParticles
tsParticles.load("tsparticles", {
    fpsLimit: 120,
    fullScreen: {
        enable: false,
        zIndex: -1
    },
    interactivity: {
        events: {
            resize: true
        },
    },
    particles: {
        color: {
            value: ["#6366f1", "#706DE5", "#8A7AC7"],
        },
        links: {
            color: "#6366f1",
            distance: 150,
            enable: true,
            opacity: 0.5,
            width: 1,
        },
        collisions: {
            enable: true,
        },
        move: {
            direction: "none",
            enable: true,
            outMode: "bounce",
            random: false,
            speed: 1,
            straight: false,
        },
        number: {
            density: {
                enable: true,
                value_area: 800,
            },
            value: 80,
        },
        opacity: {
            value: 0.5,
        },
        shape: {
            type: "circle",
        },
        size: {
            random: true,
            value: 5,
        },
    },
    detectRetina: true,
});
