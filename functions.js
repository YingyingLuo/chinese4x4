function readAloud(rowNum) {
  rowNum = rowNum.toString();
  let toSay = "";
  var cells = document.querySelectorAll("#row_" + rowNum + " td.char");
  for (var cell of cells) {
    toSay = toSay + cell.textContent;
  }
  canWeSpeak();
  speak(toSay);
}

function canWeSpeak()
{
  // Firefox is known to support only English languages on Windows, https://stackoverflow.com/questions/43983845/speechsynthesis-api-for-chinese-firefox
  // as demonstrated here https://mdn.github.io/dom-examples/web-speech-api/speak-easy-synthesis/
  //
  // This function is meant to detect mute, but has false positive on Android Chrome.
  // We may eventually switch to a more reliable detection implemented by
  // https://dev.to/jankapunkt/cross-browser-speech-synthesis-the-hard-way-and-the-easy-way-353
  var voices = window.speechSynthesis.getVoices();
  var neededVoices = voices.find(voice => voice.lang.startsWith("zh-CN"));
  if(neededVoices === undefined) {
    // Since the detection is unreliable, we shall not use alert(...).
    console.log("Your browser may not speak Chinese. Please use Chrome, Edge or Safari. Voices detected:", voices);
  }
}

function speak(speech) {
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

