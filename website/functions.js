function readAloud(rowNum) {
  rowNum = rowNum.toString();
  let toSay = "";
  var row = document.getElementById("row_" + rowNum);
  for (var i = 0, cell; cell = row.cells[i]; i++) {
    if (cell.className.indexOf("char") !== -1) {
      toSay = toSay + cell.textContent;
    }
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