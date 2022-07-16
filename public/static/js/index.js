const imgs = [
    "static/img/bongo-cat-codes-2jamming.png",
    "static/img/computer-store-landing-page.png",
    "static/img/generative-kong-summit-patterns.png",
    "static/img/responsive-social-platform-ui.png"
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
