import tkinter
import tkinter.font
from tokens import tokenize
from tokens import Text
from tokens import Tag

WIDTH, HEIGHT = 800, 600
HSTEP = 13
VSTEP = 18
SCROLL_STEP = 100

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.scroll = 0
        self.display_list = []

        self.window.bind("<Down>", self.scroll_down)
        self.window.bind("<Up>", self.scroll_up)

    def load(self, url):
        body = url.request()
        tokens = tokenize(body)
        layout = Layout(tokens)
        self.display_list = layout.display_list
        self.draw()

    def draw(self):
        self.canvas.delete("all")

        for x, y, word, font in self.display_list:
            y -= self.scroll
            if y < 0 or y > HEIGHT:
                continue

            self.canvas.create_text(
                x, y, text=word, font=font, anchor="nw"
            )

    def scroll_down(self, event):
        self.scroll += SCROLL_STEP
        self.draw()

    def scroll_up(self, event):
        self.scroll = max(0, self.scroll - SCROLL_STEP)
        self.draw()

class Layout:
    def __init__(self, root):
        self.display_list = []

        self.cursor_x = HSTEP
        self.cursor_y = VSTEP

        self.size = 12
        self.weight = "normal"
        self.slant = "roman"

        self.walk(root)

    def walk(self, node):
        if isinstance(node, Text):
            for word in node.text.split():
                self.word(word)
        else:
            self.open_tag(node.tag)
            for child in node.children:
                self.walk(child)
            self.close_tag(node.tag)

    def font(self):
        return tkinter.font.Font(
            size=self.size,
            weight=self.weight,
            slant=self.slant,
        )

    def word(self, word):
        font = self.font()
        width = font.measure(word)

        if self.cursor_x + width > WIDTH - HSTEP:
            self.cursor_x = HSTEP
            self.cursor_y += VSTEP

        self.display_list.append(
            (self.cursor_x, self.cursor_y, word, font)
        )

        self.cursor_x += width + font.measure(" ")

    def open_tag(self, tag):
        if tag == "b":
            self.weight = "bold"
        elif tag == "i":
            self.slant = "italic"
        elif tag == "small":
            self.size -= 2
        elif tag == "big":
            self.size += 4
        elif tag == "br":
            self.cursor_x = HSTEP
            self.cursor_y += VSTEP

    def close_tag(self, tag):
        if tag == "b":
            self.weight = "normal"
        elif tag == "i":
            self.slant = "roman"
        elif tag == "small":
            self.size += 2
        elif tag == "big":
            self.size -= 4