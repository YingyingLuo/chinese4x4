function readAloud(rowNum) {
  rowNum = rowNum.toString();
  let toSay = "";
  var cells = document.querySelectorAll("#row_" + rowNum + " td.char");
  for (var cell of cells) {
    toSay = toSay + cell.textContent;
  }
  let utterance = new SpeechSynthesisUtterance(toSay);
  utterance.lang = "zh-CN";
  speechSynthesis.speak(utterance);
};

function toggleColumn(colClassName) {
  const cells = document.getElementsByClassName(colClassName);
  for (var cell of cells) {
    if (cell.style.display === "none") {
      cell.style.display = "";
    } else {
      cell.style.display = "none";
    }
  }
};

function toggleColumnWithButton(colClassName, buttonID) {
  toggleColumn(colClassName);

  const button = document.getElementById(buttonID);
  if (button.textContent.substring(0, 4) === "Hide") {
    button.textContent = "Show" + button.textContent.substring(4);
  } else {
    button.textContent = "Hide" + button.textContent.substring(4);
  }
};