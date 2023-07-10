from browser import document, bind, html, window
from random import shuffle

# Note: If you could avoid unnecessary import, your script will save several seconds loading time
# For example, use `"message".title()` instead of `import string; string.capwords("message")`

initial_chars = "一知半解一心一意一丘之貉一目了然"
initial_defs = [
    "A little knowledge is a dangerous thing.",
    "John is a person who always works with undivided attention.",
    "These people are cut from the same cloth.",
    "His words just leapt to the eye.",
]
initial_pinyin = [
    "yì zhī bàn jiě",
    "yì xīn yí yì",
    "yì qiū zhī hé",
    "yí mù liǎo rán",
]

def get_list(string, chars_per_elem):
    return [string[i:i + chars_per_elem] for i in range(0, len(string), chars_per_elem)]

def fill(cell_selector, words):
    for i, cell in enumerate(document.select(cell_selector)):
        cell.text = words[i] if i < len(words) else ""

fill("#table td.pinyin", initial_pinyin)
fill("#table td.def", initial_defs)
for i in range(16):  # Predefine all cards
    document["cards"].attach(html.SPAN(
        "",
        id="card{}".format(i),
        draggable=True,
        Class="shadow",
        ))

CARDS = "#cards span"  # Cards are predefined, we can bind events to them once and for all

@bind(CARDS, "mouseover")
def mouseover(event):
    event.target.style.cursor = "pointer"

@bind(CARDS, "dragstart")
def dragstart(event):
    event.dataTransfer.setData("dragged", event.target.id)  # data has to be a string

BOARD = "#table td.char"

@bind(BOARD, "dragover")
def dragover(event):
    event.dataTransfer.dropEffect = "move"
    event.preventDefault()

@bind(BOARD, "drop")
def drop(event):
    character = document[event.dataTransfer.getData("dragged")]
    if isinstance(event.target, html.SPAN):  # Turns out sub-SPAN is also droppable
        event.target.text, character.text = character.text, event.target.text
    elif isinstance(event.target, html.TD):
        target_cards = event.target.select("span")
        if target_cards:
            target_cards[0].text, character.text = character.text, target_cards[0].text
        else:
            event.target.attach(html.SPAN(character.text, Class="shadow"))
            character.text = ""
    event.preventDefault()

def chars_per_cell(stage):
    return [4, 2, 1][stage - 1]

def _set_stage(stage):
    assert stage in [1, 2, 3], f"We only accept 1 or 2 or 3 but you chose {stage}"
    one_char_cell_w = 1.2
    cell_selector = f"#table td.stage_{stage}"
    for cell in document.select(BOARD):
        cell.text = ""
        is_cell_of_current_stage = f"stage_{stage}" in cell.Class().split()
        cell.style.display = "" if is_cell_of_current_stage else "none"
    for cell in document.select(cell_selector):
        cell.style.width = str(one_char_cell_w * chars_per_cell(stage)) + "em"
    fill(cell_selector, get_list(initial_chars, chars_per_cell(stage)))  # sets the table
    fill("#cards span", [""] * 16)  # Clean up all cards

_set_stage(1)  # Set stage 1 by default

# Note: If they are defined inside html, it turns out refresh page won't reset them to disabled.
document.select_one("button.starter[value='2']").disabled = True
document.select_one("button.starter[value='3']").disabled = True
document.select_one("#stage_4_button").disabled = True
document.select_one("#check").disabled = True

@bind("button.starter", "click")
def starter(event):
    stage = int(event.target.value)
    _set_stage(stage)
    fill(BOARD, [""] * 16)
    cards = get_list(initial_chars, chars_per_cell(stage))
    shuffle(cards)
    fill(CARDS, cards)
    document.select_one("#check").disabled = False
    document["result"].text = "Drag and drop cards on the left into the table, and then check your work"


@bind("#stage_4_button", "click")
def stage_4(event):
    _set_stage(3)  # The stage 4 board has same 4x4 setup as stage 3
    for cell in document.select("#table td.stage_3"):
        text = cell.text
        cell.text = ""  # It would also clean up its child
        cell.attach(html.SPAN(text, Class=" ".join([
            "shadow",  # For shadow effect
            "char",  # So that the speaker button can still work
            "flip",  # For the flip effect
            ])))

    @bind(".flip", "click")
    def flip(event):
        event.target.style.color = "white" if event.target.style.color != "white" else "black"

    @bind(".flip", "dblclick")
    def speak(event):
        window.speak(event.target.text)  # Calling a function defined in Javascript
        # Known issue: After double-click, the text would be selected therefore visible

@bind("#check", "click")
def check(event):
    # Relies on the number of visible board cells to auto-detect the stage
    visible_cells = document.select(
        # The selector is inspired from https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors#languages
        # Seems fragile, though. For example, the space in the selector must be there.
        BOARD + ':not([style*="display: none"])')
    expected = get_list(initial_chars, 16 // len(visible_cells))
    actual = [cell.text for cell in visible_cells]
    pairs = zip(expected, actual)
    wrong_count = sum(1 if e != a else 0 for e, a in pairs)
    if wrong_count:
        document["result"].text = f"{wrong_count} item(s) are in the wrong place."
    else:
        current_stage = {4: 1, 8: 2, 16: 3}[len(visible_cells)]
        document["result"].text = "Correct! Next stage is now unlocked."
        if current_stage < 3:
            document.select(f'button.starter[value="{current_stage+1}"]')[0].disabled = False
        else:
            document.select_one("#stage_4_button").disabled = False

