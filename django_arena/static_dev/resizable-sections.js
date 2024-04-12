$(function () {
  var resizer1 = $("#resizer1");
  var resizer2 = $("#resizer2");
  var resizer3 = $("#resizer3");

  var column1 = $("#column1");
  var column2 = $("#column2");
  var column3 = $("#column3");

  var code = $("#code-section");
  var tests = $("#tests-section");

  resizer1.mousedown(function (e) {
    var startX = e.pageX;
    var initialWidth1 = column1.width();
    var initialWidth2 = column2.width();

    $(document).mousemove(function (e) {
      var newWidth1 = initialWidth1 + (e.pageX - startX);
      var newWidth2 = initialWidth2 - (e.pageX - startX);

      column1.width(newWidth1);
      column2.width(newWidth2);
    });

    $(document).mouseup(function () {
      $(document).off("mousemove");
    });
  });

  resizer2.mousedown(function (e) {
    var startX = e.pageX;
    var initialWidth2 = column2.width();
    var initialWidth3 = column3.width();

    $(document).mousemove(function (e) {
      var newWidth2 = initialWidth2 + (e.pageX - startX);
      var newWidth3 = initialWidth3 - (e.pageX - startX);

      column2.width(newWidth2);
      column3.width(newWidth3);
    });

    $(document).mouseup(function () {
      $(document).off("mousemove");
    });
  });

  resizer3.mousedown(function (e) {
    var startY = e.pageY;
    var initialWidth1 = code.height();
    var initialWidth2 = tests.height();

    $(document).mousemove(function (e) {
      var newWidth1 = initialWidth1 + (e.pageY - startY);
      var newWidth2 = initialWidth2 - (e.pageY - startY);

      code.height(newWidth1);
      tests.height(newWidth2);
    });

    $(document).mouseup(function () {
      $(document).off("mousemove");
    });
  });
});
