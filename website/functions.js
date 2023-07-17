function readAloud(rowNum) {
  rowNum = rowNum.toString();
  let toSay = "";
  var cells = document.querySelectorAll("#row_" + rowNum + " td.char");
  for (var cell of cells) {
    toSay = toSay + cell.textContent;
  }
  speak(toSay);
}

function speak(speech) {
  var voices = window.speechSynthesis.getVoices();
  var neededVoices = voices.find(voice => voice.lang.startsWith("zh-CN"));
  if(neededVoices === undefined) {
    console.log(voices);
    // Firefox is known to support only English languages on Windows, https://stackoverflow.com/questions/43983845/speechsynthesis-api-for-chinese-firefox
    // as demonstrated here https://mdn.github.io/dom-examples/web-speech-api/speak-easy-synthesis/
    alert("Your browser does not speak Chinese. Please switch to Chrome, Edge or Safari.");
  }

  let utterance = new SpeechSynthesisUtterance(speech);
  utterance.lang = "zh-CN";
  speechSynthesis.speak(utterance);
}

function toggleColumn(colClassName) {
  const cells = document.getElementsByClassName(colClassName);
  for (var cell of cells) {
    if (cell.style.display === "none") {
      cell.style.display = "";
    } else {
      cell.style.display = "none";
    }
  }
}

function toggleColumnWithButton(colClassName, buttonID) {
  toggleColumn(colClassName);

  const button = document.getElementById(buttonID);
  if (button.textContent.substring(0, 4) === "Hide") {
    button.textContent = "Show" + button.textContent.substring(4);
  } else {
    button.textContent = "Hide" + button.textContent.substring(4);
  }
}

