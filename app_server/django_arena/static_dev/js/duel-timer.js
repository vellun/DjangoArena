$.ajax({
  type: "GET",
  url: timer_url,
  data: {
    duration: duration,
  },
  success: function (response) {
    var timerData = response.split(":");
    var hours = parseInt(timerData[0]);
    var minutes = parseInt(timerData[1]);
    var seconds = parseInt(timerData[2]);
    $("#timer").text(
      (hours < 10 ? "0" : "") +
        hours +
        ":" +
        (minutes < 10 ? "0" : "") +
        minutes +
        ":" +
        (seconds < 10 ? "0" : "") +
        seconds
    );
  },
  error: function (error) {
    console.log("Error:", error);
  },
});

function updateTimer() {
  var hours = parseInt($("#timer").text().split(":")[0]);
  var minutes = parseInt($("#timer").text().split(":")[1]);
  var seconds = parseInt($("#timer").text().split(":")[2]);

  if (seconds > 0) {
    seconds--;
  } else {
    if (minutes > 0) {
      minutes--;
      seconds = 59;
    } else {
      if (hours > 0) {
        hours--;
        minutes = 59;
        seconds = 59;
      } else {
        $.ajax({
          type: "POST",
          url: timer_url,
          data: {
            type: "redirect",
            csrfmiddlewaretoken: csrf_token,
          },
          success: function (response) {
            window.location.href = redirect_url;
          },
          error: function (error) {
            console.log("Error:", error);
          },
        });
      }
    }
  }
  $("#timer").text(
    (hours < 10 ? "0" : "") +
      hours +
      ":" +
      (minutes < 10 ? "0" : "") +
      minutes +
      ":" +
      (seconds < 10 ? "0" : "") +
      seconds
  );
  $.ajax({
    type: "POST",
    url: timer_url,
    data: {
      csrfmiddlewaretoken: csrf_token,
      type: "cache",
      timer: $("#timer").text(),
    },
    success: function (response) {},
    error: function (error) {
      console.log("Error:", error);
    },
  });
}

setInterval(updateTimer, 1000);
