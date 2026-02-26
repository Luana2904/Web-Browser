import sys
import tkinter
from Elementos.window import Browser
from Elementos.url import URL
from Elementos.tokens import HTMLParser

if __name__ == "__main__":
    browser = Browser()
    browser.load(URL(sys.argv[1]))
    tkinter.mainloop()

    body = URL(sys.argv[1]).request()
    nodes = HTMLParser(body).parse()
    HTMLParser.print_tree(nodes)