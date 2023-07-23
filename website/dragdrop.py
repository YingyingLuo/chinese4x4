from browser import html

class Card(html.SPAN):
    def __init__(self, text):
        super(self.__class__, self).__init__(text, Class="shadow", draggable=True)