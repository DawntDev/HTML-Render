<h1>HTML-Render</h1>
<p>
 <a href="https://discord.gg/mexicodev">
     <img alt="Dawnt | Discord" width="24px" align="right" raw=true HSPACE="5" src="https://discord.com/assets/847541504914fd33810e70a0ea73177e.ico"></a>
 <a href="https://open.spotify.com/playlist/6eDl0FX1pNcaFXgYIBOobX?si=aewrQ2nJTuSgkMSip3d8-Q&utm_source=copy-link">
     <img alt="Dawnt | Spotify" width="24px" align="right" raw=true HSPACE="5" src="https://open.spotifycdn.com/cdn/images/favicon.5cb2bd30.ico"></a>
 <a href="https://www.codewars.com/users/Dawnt">
    <img alt="Dawnt | CodeWars" width="24px" align="right" raw=true HSPACE="5" src="https://www.codewars.com/packs/assets/logo.61192cf7.svg"></a>
 <a href="mailto:jmanuelhv9@gmail.com">
    <img alt="Dawnt | Email" width="24px" align="right" raw=true HSPACE="5" src="https://ssl.gstatic.com/ui/v1/icons/mail/rfr/gmail.ico"></a>
</p>

<h3>About</h3>

HTML-Render is an API whose main purpose is to convert HTML and CSS into an image, which can be used by the user.
I created this API because I wanted to put into practice my knowledge with the [Flask](https://flask.palletsprojects.com/en/2.1.x/) framework. Also, the API format makes it easy to implement with other technologies and languages, and the quality of the images is very good.


<!-- TABLE OF CONTENTS -->

## Table of Contents

-   [Overview](#overview)
-   [Features](#features)
-   [How to use](#how-to-use)
-   [Contributions](#contributions)
-   [Acknowledgements](#acknowledgements)

<!-- OVERVIEW -->

## Overview

<div align="center">
    <img src="https://raw.githubusercontent.com/DawntDev/HTML-Render/master/public/static/img/bongo-cat-codes-2jamming.webp" width="35%" raw=false>
    <img src="https://raw.githubusercontent.com/DawntDev/HTML-Render/master/public/static/img/computer-store-landing-page.webp" width="35%" raw=false>
    <img src="https://raw.githubusercontent.com/DawntDev/HTML-Render/master/public/static/img/generative-kong-summit-patterns.webp" width="35%" raw=false>
    <img src="https://raw.githubusercontent.com/DawntDev/HTML-Render/master/public/static/img/responsive-social-platform-ui.webp" width="35%" raw=false>
</div>

The project was created with [Flask](https://flask.palletsprojects.com/en/2.1.x/) in addition to the use of the [Selenium](https://www.selenium.dev/) library for rendering of images.

-   Functioning
    -   The operation is simple, with [Flask](https://flask.palletsprojects.com/en/2.1.x/) we create a server in which we will be hosting the html files, which we want to render. And by means of a request to the same server with [Selenium](https://www.selenium.dev/) we obtain an image of the DOM.
-   Use of [Flask](https://flask.palletsprojects.com/en/2.1.x/)
    -   Flask is a framework that allows us to create web applications in an easy way. Thanks to this we were able to create a web application. That by means of dynamic paths will host the HTML files, giving them a unique ID.<br>These files were obtained through GET and POST requests, which vary depending on the type of element to be rendered (an active web page or the raw html code).
-   Use of [Selenium](https://www.selenium.dev/)
    -   Thanks to the selenium library I was able to get a representation of the DOM, plus some extra options such as being able to select a specific element or the dimensions of the capture.
-   What I learned
    -   During the development of this project I reinforced and applied my knowledge of the [Flask](https://flask.palletsprojects.com/en/2.1.x/) framework. Among them the use of dynamic paths, which render specific files.

## Features

Its main function is to render raw html code and active web pages. It also has a web interface to simplify API usage.

Functions:
-   ### Render HTML code
    -   With this function you can render your own HTML, CSS and JavaScript code. This in order to give as much customization as possible to the DOM. 

-   ### Render Webpage
    -   With this functionality you will be able to render any web page simply using the URL of that page. Note that since the rendering of this page is done from a [headless browser](https://en.wikipedia.org/wiki/Headless_browser), you will not see any of the styles that the page allows you to customize as a user.

## How To Use

The API is accessible from two different URLs:
-   `url/api/v1/render`
-   `url/api/v1/urlToImage`

These two routes share a strong resemblance in the body of their request. Which is an object with the following structure.

```typescript
{
    selector: string,
    format: string, 
    size: Array<string>,
    timeout: float,
}
```
Only certain elements are added to this object, depending on the path used.

**render**:
For this path, only three more elements need to be added to the object, which are as follows.
```typescript
{
    elements: string,
    css: string,
    js: string,
}
```
**urlToImage**:
For this path, only one more element needs to be added to the object, which is as follows.
```typescript
{
    url: string,
}
```

### Options

-   **selector**: CSS selector of the element you want to render.

-   **format**: Format of the image. It can be either `png`, `jpg`, `bin` o `base64`.

-   **size**: Size of the image. This can be a value in pixels or `full`, the latter is a dynamic measurement which is based on the maximum size of the element you have selected.

-   **timeout**: Waiting time to take the capture, this starts counting from the moment the server renders the page.

-   **elements**: HTML code of the elements you want to render. Only from the body

-   **css**: CSS code of the elements you want to render.

-   **js**: JavaScript code of the elements you want to render.

-   **url**: URL of the webpage you want to render.


### Default values

-   **selector**: `body`

-   **format**: `png`

-   **size**: [`1920`, `1080`]

-   **timeout**: `2.5`


## Contributions

**If you wish to contribute to the development of the extension:**

-   First clone the repository
    ```bash
    git clone https://github.com/DawntDev/HTML-Render.git
    ```
-   Then create a branch with your user name
    ```bash
    git checkout -b <your-user-name>
    ```
-   Install project dependencies
    ```bash
    pip install -r requirements.txt
    ```
    Pull requests are welcome, I would appreciate your support to contribute to a better development of this application. For major changes, please open an issue to discuss what you would like to change.


<div align="center">

[![Flask](https://img.shields.io/badge/Made%20with%20Flask-61DAFB.svg?style=for-the-badge&color=000&logo=flask&logoColor=fff)](https://flask.palletsprojects.com/en/2.1.x/)

</div>
