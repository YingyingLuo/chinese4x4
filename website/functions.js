const readAloud = function(rowNum) {
  rowNum = rowNum.toString();
  let toSay = "";
  for (let i = 1; i <= 4; i++) {
    toSay = toSay + document.getElementById(rowNum + i.toString()).textContent;
  }
  let utterance = new SpeechSynthesisUtterance(toSay);
  utterance.lang = "zh-CN";
  speechSynthesis.speak(utterance);
};

const toggleColumn = function(col_class_name) {
  const cells = document.getElementsByClassName(col_class_name);
  for (var cell of cells) {
    if (cell.style.display === "none") {
      cell.style.display = "";
    } else {
      cell.style.display = "none";
    }
  }
};

const toggleColumnWithButton = function(col_class_name, button_id) {
  toggleColumn(col_class_name);

  const button = document.getElementById(button_id);
  if (button.textContent.substring(0, 4) === "Hide") {
    button.textContent = "Show" + button.textContent.substring(4);
  } else {
    button.textContent = "Hide" + button.textContent.substring(4);
  }
};