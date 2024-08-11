var editor = CodeMirror.fromTextArea(document.getElementById("id_code"), {
  mode: "python",
  lineNumbers: true,
  autoCloseBrackets: true,
  matchBrackets: true,
  lineWrapping: true,
  indentUnit: 4,
  theme: "dracula",
});

editor.on("change", function () {
  $.ajax({
    url: cache_url,
    type: "POST",
    data: {
      code: editor.getValue(),
      task_num: task_num,
      csrfmiddlewaretoken: csrf_token,
    },
    success: function (data) {
      console.log("Code cached successfully");
    },
    error: function (xhr, textStatus, errorThrown) {
      console.log("Error caching code: " + errorThrown);
    },
  });
});
