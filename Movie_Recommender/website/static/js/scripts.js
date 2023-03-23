/*!
* Start Bootstrap - The Big Picture v5.0.5 (https://startbootstrap.com/template/the-big-picture)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-the-big-picture/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

window.addEventListener("load", function() {
    const images = document.querySelectorAll(".movie_container img");
  });

const submitButton = document.querySelector("#submit");
submitButton.addEventListener("click", function() {
  const images = document.querySelectorAll(".movie_container img");
  images.forEach(image => {
    image.style.animationName = "fadeOut";
    image.style.animationDuration = "1s";
    image.style.animationFillMode = "forwards";
  });
});