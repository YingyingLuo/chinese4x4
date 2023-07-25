from browser import html

def mouseover(event):
    event.target.style.cursor = "pointer"

def dragstart(event):
    event.dataTransfer.setData("dragged", event.target.id)  # data has to be a string

builtin_id = id

class Card(html.SPAN):
    def __init__(self, text, id=None, Class=None):
        if not id:
            id = f"id_{builtin_id(self)}"
        super(self.__class__, self).__init__(text, id=id, Class=Class, draggable=True)
        self.bind("mouseover", mouseover)
        self.bind("dragstart", dragstart)
