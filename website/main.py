from browser import document, bind, html
from random import shuffle

# Note: If you could avoid unnecessary import, your script will save several seconds loading time
# For example, use `"message".title()` instead of `import string; string.capwords("message")`

idiom_sets = {
    "一知半解": ("yī zhī bàn jiě", "To have only half the knowledge, like an amateur"),
    "一心一意": ("yī xīn yī yì", "To work with undivided attention"),
    "一丘之貉": ("yī qiū zhī hé", "Jackals from the same hill (they are all just as bad as each other)"),
    "一目了然": ("yī mù liǎo rán", "Obvious at a glance"),
    "笨鸟先飞": ("bèn niǎo xiān fēi", "The clumsy bird must start flying early (work hard to compensate for less ability)"),
    "一帆风顺": ("yī fān fēng shùn", "Smooth sailing"),
    "一刻千金": ("yī kè qiān jīn", "Time is gold"),
    "一事无成": ("yī shì wú chéng", "To have achieved nothing"),
    "一败涂地": ("yī bài tú dì", "To suffer a crushing defeat"),
    "一清二楚": ("yī qīng èr chǔ", "Very clear"),
    "一意孤行": ("yī yì gū xíng", "Stubbornly sticking to one's own way"),
    "一落千丈": ("yī luò qiān zhàng", "To suffer a sudden big decline"),
    "一鸣惊人": ("yī míng jīng rén", "To shock the world with one birdcall (become a celebrity overnight) "),
    "一诺千金": ("yī nuò qiān jīn", "A promise worth a thousand gold pieces (a promise that must be kept)"),
    "一蹴可及": ("yī cù kě jí", "To succeed on the first try"),
    "一筹莫展": ("yī chóu mò zhǎn", "Unable to find a solution, exhausted all ideas"),
    "一览无遗": ("yī lǎn wú yí", "Plainly visible"),
    "一窍不通": ("yī qiào bù tōng", "Didn't understand a single word"),
    "九死一生": ("jiǔ sǐ yī shēng", "To make a narrow escape"),
    "九牛一毛": ("jiǔ niú yī máo", "A single hair out of nine oxen (a very small portion)"),
    "人生如梦": ("rén shēng rú mèng", "Life is but a dream"),
    "人定胜天": ("rén dìng shèng tiān", "Man can conquer nature"),
    "人山人海": ("rén shān rén hǎi", "Mountains and oceans of people (a vast crowd)"),
    "人之常情": ("rén zhī cháng qíng", "Human nature"),
    "人云亦云": ("rén yún yì yún", "To follow the majority"),
    "人去楼空": ("rén qù lóu kōng", "The people are gone and the place is deserted"),
    "人面兽心": ("rén miàn shòu xīn", "Face of a human but heart of a beast (evil under the surface)"),
    "人言可畏": ("rén yán kě wèi", "Gossip is a frightening thing"),
    "十全十美": ("shí quán shí měi", "Complete and beautiful, perfect"),
    "十拿九稳": ("shí ná jiǔ wěn", "Of ten attempts, nine will succeed (success is almost certain)"),
    "十万火急": ("shí wàn huǒ jí", "Very urgent"),
    "力不从心": ("lì bù cóng xīn", "The mind wants to but the body is too weak"),
    "力挽狂澜": ("lì wǎn kuáng lán", "To work against a strong tide (to work hard against a severe crisis)"),
    "入乡随俗": ("rù xiāng suí sú", "Follow the local customs"),
    "入木三分": ("rù mù sān fēn", "The writing is profound"),
    "七上八下": ("qī shàng bā xià", "Emotionally upset"),
    "七窍生烟": ("qī qiào shēng yān", "Spouting smoke (very angry)"),
    "七零八落": ("qī líng bā luò", "Everything is broken and in ruins"),
    "八面玲珑": ("bā miàn líng lóng", "Good at forming social relations with ease"),
    "千钧一发": ("qiān jūn yī fà", "A thousand pounds hangs by a single thread (a dangerous situation)"),
    "大智若愚": ("dà zhì ruò yú", "Great intelligence may seem like stupidity"),
    "大器晚成": ("dà qì wǎn chéng", "Great talent takes a long time to achieve"),
    "大海捞针": ("dà hǎi lāo zhēn", "Looking for a needle in a haystack (an impossible search)"),
    "山穷水尽": ("shān qióng shuǐ jìn", "Mountains and rivers have been exhausted (ran out of resources)"),
    "小题大做": ("xiǎo tí dà zuò", "To make a big deal over nothing"),
    "亡羊补牢": ("wáng yáng bǔ láo", "To fix the pen after the sheep have been lost (to fix a problem too late)"),
    "不辞而别": ("bù cí ér bié", "To leave without saying goodbye"),
    "少年老成": ("shào nián lǎo chéng", "Young but mature"),
    "毛遂自荐": ("máo suì zì jiàn", "To recommend or promote one's own services"),
    "心满意足": ("xīn mǎn yì zú", "Content and satisfied"),
    "文胜于武": ("wén shèng yú wǔ", "The pen is mightier than the sword (writing has more power than violence)"),
    "以身作则": ("yǐ shēn zuò zé", "To lead by example"),
}

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
    print(event.target)
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
        if current_stage < 3:
            document.select(f'button.starter[value="{current_stage+1}"]')[0].disabled = False
            document["result"].text = "Correct! Next stage is now unlocked."
        else:
            document["result"].text = "Congratulations! You have cleared 3 stages!"

