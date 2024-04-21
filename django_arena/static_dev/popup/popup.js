const modal = new bootstrap.Modal(document.getElementById("modal"), {
  backdrop: 'static'
})

htmx.on("htmx:afterSettle", (e) => {
  const response = JSON.parse(e.detail.xhr.responseText);

  if (response.success) {
      modal.hide();

      const link = response.link;
      if (link) {
          window.location.href = link;
      }
  }
});


htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #dialog => show the modal
  if (e.detail.target.id == "dialog") {
    modal.show()
  }
})

htmx.on("htmx:beforeSwap", (e) => {
  // Empty response targeting #dialog => hide the modal
  if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
    modal.hide()
    e.detail.shouldSwap = false
  }
})

htmx.on("hidden.bs.modal", () => {
  document.getElementById("dialog").innerHTML = ""
})



