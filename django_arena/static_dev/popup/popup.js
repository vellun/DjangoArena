document.addEventListener("DOMContentLoaded", function () {
  var popupForm = document.getElementById("popup-form");
  var openPopupBtn = document.getElementById("open-popup");
  var closePopupBtn = document.querySelector(".close");

  openPopupBtn.onclick = function () {
    loadForm();
    popupForm.style.display = "block";
  };

  closePopupBtn.onclick = function () {
    popupForm.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target == popupForm) {
      popupForm.style.display = "block";
    }
  };

  function loadForm() {
    var formContainer = document.getElementById("settings-form");
    while (formContainer.firstChild) {
      formContainer.removeChild(formContainer.firstChild);
    }

    fetch(settings_url)
      .then((response) => response.text())
      .then((html) => {
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, "text/html");
        var formElement = doc.getElementById("settings-form");
        formContainer.appendChild(formElement);
      });
  }
});

