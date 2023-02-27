from browser import document, bind, html
from copy import deepcopy
from random import shuffle

# Note: If you could avoid unnecessary import, your script will save several seconds loading time
# For example, use `"message".title()` instead of `import string; string.capwords("message")`

one_char_cell_w = 1.2

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

# initial default values (a Java convention)
cell_selector = ""
chars_per_cell = 0
chars_list = []

# methods relying on input arguments

def toggle_column(col_class_name):
    for cell in document.select(col_class_name):
        cell.style.display = "" if cell.style.display == "none" else "none"

def get_list(string, chars_per_elem):
    l = []
    for i in range(int(len(string) / chars_per_elem)):
        l.append(string[i * chars_per_elem:i * chars_per_elem + chars_per_elem])
    return l

# methods relying on global variables

def set_table():
    for i, cell in enumerate(document.select(cell_selector)):
        cell.text = chars_list[i]

def write_pinyin():
    for i, cell in enumerate(document.select("#table td.pinyin")):
        cell.text = initial_pinyin[i]

def write_definitions():
    for i, cell in enumerate(document.select("#table td.def")):
        cell.text = initial_defs[i]

def create_empty_cards():
    for i in range(int(len(initial_chars) / chars_per_cell)):   # TODO: consider changing to for i in range(len(get_list(...)))
        document["cards"].attach(html.SPAN("", id="card{}".format(i), draggable=True))

@bind("#start", "click")
def start(event):
    document["start"].text = "Restart"

    for cell in document.select(cell_selector):
        cell.text = ""

    cards = deepcopy(chars_list)
    shuffle(cards)
    for i, c in enumerate(cards):
        document["card" + str(i)].text = c

@bind("#check", "click")
def check(event):
    wrong_count = 0
    for i, cell in enumerate(document.select(cell_selector)):
        if chars_list[i] != cell.text:
            wrong_count = wrong_count + 1

    document["result"].text = (
        str(wrong_count) + " item(s) are in the wrong place."
        ) if wrong_count != 0 else "Correct!"

def mouseover(event):
    event.target.style.cursor = "pointer"

def dragstart(event):
    event.dataTransfer.setData("character", event.target.id)

def make_cards_draggable():
    for card in document.select("#cards span"):
        card.bind("mouseover", mouseover)
        card.bind("dragstart", dragstart)

def dragover(event):
    event.dataTransfer.dropEffect = "move"
    event.preventDefault()

def drop(event):
    character = document[event.dataTransfer.getData("character")]
    to_replace = event.target.text
    event.target.text = character.text
    character.text = to_replace
    event.preventDefault()

def make_cells_droppable():
    for cell in document.select(cell_selector):
        cell.bind("dragover", dragover)
        cell.bind("drop", drop)

cell_selector = "#table td.round_1"
chars_per_cell = 4
chars_list = get_list(initial_chars, chars_per_cell)

write_pinyin()
write_definitions()

toggle_column("#table td.char")     # hide all cells
toggle_column(cell_selector)        # show relevant cells
for cell in document.select(cell_selector):
    cell.style.width = str(one_char_cell_w * chars_per_cell) + "em"

set_table()
create_empty_cards()
make_cards_draggable()
make_cells_droppable()