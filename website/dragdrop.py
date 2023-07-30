from browser import html

def mouseover(event):
    event.target.style.cursor = "pointer"

def dragstart(event):
    event.dataTransfer.setData("dragged", event.target.id)  # data has to be a string

builtin_id = id

class Card(html.SPAN):
    times_flipped = 0

    def __init__(self, text, id=None, Class=None):
        if not id:
            id = f"id_{builtin_id(self)}"
        super(self.__class__, self).__init__(text, id=id, Class=Class, draggable=True)
        self.bind("mouseover", mouseover)
        self.bind("dragstart", dragstart)

#    def flipped_once(self):
#        self.times_flipped = 12


print(type(Card))
print(Card.times_flipped)
Card.times_flipped = "some value"
print(Card.times_flipped)

c1 = Card("sample text")
print(type(c1))
print(c1.times_flipped)
c1.times_flipped = "new value"
print(c1.times_flipped)