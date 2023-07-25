from browser import html

def mouseover(event):
    event.target.style.cursor = "pointer"

def dragstart(event):
    event.dataTransfer.setData("dragged", event.target.id)  # data has to be a string

class Card(html.SPAN):
    def __init__(self, text, Class=None):
        super(self.__class__, self).__init__(text, id=f"id_{id(self)}", Class=Class, draggable=True)
        self.bind("mouseover", mouseover)
        self.bind("dragstart", dragstart)