formCounter = 2;
$("#new-choice").on("click", function () {
  form =
    "<p><label for='id_choices-" +
    formCounter +
    "-choice_text'>Choice text:</label> <input type='text' name='choices-" +
    formCounter +
    "-choice_text' maxlength='255' id='id_choices-" +
    formCounter +
    "-choice_text'></p>";
  form +=
    "<p><label for='id_choices-" +
    formCounter +
    "-DELETE'>Delete:</label> <input type='checkbox' name='choices-" +
    formCounter +
    "-DELETE' id='id_choices-" +
    formCounter +
    "-DELETE'><input type='hidden' name='choices-" +
    formCounter +
    "-id' id='id_choices-" +
    formCounter +
    "-id'><input type='hidden' name='choices-" +
    formCounter +
    "-question' id='id_choices-" +
    formCounter +
    "-question'></p>";
  $("#new-choice").before(form);
  formCounter++;
  $("#id_choices-TOTAL_FORMS").val(formCounter);
});
