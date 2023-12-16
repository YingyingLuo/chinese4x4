from browser import document, bind, html, window, ajax
from random import shuffle
import csv
import brython_dragdrop as dragdrop


class Card(dragdrop.DraggableMixin, html.SPAN):
    pass


initial_chars = "一知半解一心一意一丘之貉一目了然"  # Placeholder
BOARD = "#table td.char"
# Make the dragged elements droppable, based on rules
dragdrop.make_droppable(BOARD, rules={
    (Card, Card): dragdrop.swap,
    (Card, html.TD): dragdrop.occupy,
})
dragdrop.make_droppable("#cards", rules={
    (Card, Card): dragdrop.swap,
    (Card, html.DIV): dragdrop.join,
})

# Read idioms from query string idioms=path/to/file.csv
def initialize(ajax_response):
    global initial_chars
    print(ajax_response.text)
    idioms = {}
    for row in csv.reader(ajax_response.text.splitlines()):
        idioms[row[0]] = (row[1], row[2])
    initial_chars = "".join(idioms.keys())
    fill("#table td.pinyin", [v[0] for v in idioms.values()])
    fill("#table td.def", [v[1] for v in idioms.values()])
    _set_stage(1)  # Set stage 1 by default
ajax.get(document.query.getvalue("idioms", "idioms/default.csv"), oncomplete=initialize)


def get_list(string, chars_per_elem):
    return [string[i:i + chars_per_elem] for i in range(0, len(string), chars_per_elem)]

def fill(cell_selector, words):
    for i, cell in enumerate(document.select(cell_selector)):
        cell.text = words[i] if i < len(words) else ""

for i in range(16):  # Predefine all cards
    document["cards"].attach(Card(
        "",
        id="card{}".format(i),
        Class="shadow",
        ))

CARDS = "#cards span"  # Cards are predefined, we can bind events to them once and for all

def chars_per_cell(stage):
    return [4, 2, 1][stage - 1]

def _set_stage(stage):
    assert stage in [1, 2, 3], f"We only accept 1 or 2 or 3 but you chose {stage}"
    cell_selector = f"#table td.stage_{stage}"
    for cell in document.select(BOARD):
        cell.text = ""
        is_cell_of_current_stage = f"stage_{stage}" in cell.Class().split()
        cell.style.display = "" if is_cell_of_current_stage else "none"
    fill(cell_selector, get_list(initial_chars, chars_per_cell(stage)))  # sets the table
    fill(CARDS, [""] * 16)  # Clean up all cards

@bind("button.starter", "click")
def starter(event):
    stage = int(event.target.value)
    _set_stage(stage)
    clean_up()
    cards = get_list(initial_chars, chars_per_cell(stage))
    shuffle(cards)
    fill(CARDS, cards)
    document["check"].disabled = False
    document["result"].text = "Drag and drop cards on the left into the table, and then check your work"


@bind("#stage_4_button", "click")
def stage_4(event):
    document["check"].disabled = True
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
    right_count = sum(1 if e == a else 0 for e, a in pairs)
    if right_count < len(actual):
        document["result"].text = f"Not quite! {right_count} item(s) are in the right place so far."
    else:
        current_stage = {4: 1, 8: 2, 16: 3}[len(visible_cells)]
        document["result"].text = "All correct! Next stage is now unlocked."
        if current_stage < 3:
            document.select(f'button.starter[value="{current_stage+1}"]')[0].disabled = False
        else:
            document["stage_4_button"].disabled = False
            document["stage_5_button"].disabled = False

@bind("#stage_5_button", "click")
def stage_5(event):
    document["check"].disabled = True
    clean_up()
    cards = get_list(initial_chars, 1)
    shuffle(cards)
    document["stage_5_box"].text = cards[0]

    @bind(document["stage_5_box"], "click")
    def get_next(event):
        if cards:
            document["stage_5_box"].text = cards.pop(0)
        else:
            document["stage_5_box"].text = ""
            document["result"].text = "Congrats! You have completed all stages."

def clean_up():
    # A unified helper so that old callers will also clean up residue from newly added stages
    fill(CARDS, [""] * len(initial_chars))  # Stage 1, 2, 3
    fill(BOARD, [""] * len(initial_chars))  # All stages
    document["stage_5_box"].text = ""  # For stage 5

# Note: If they are defined inside html, it turns out refresh page won't reset them to disabled.
document.select_one("button.starter[value='1']").disabled = document.query.getvalue("mode") == "review"
document.select_one("button.starter[value='2']").disabled = True
document.select_one("button.starter[value='3']").disabled = document.query.getvalue("mode") != "review"
document.select_one("#stage_4_button").disabled = True
document.select_one("#stage_5_button").disabled = True
document.select_one("#check").disabled = True
