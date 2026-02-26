class Text:
    def __init__(self, text, parent):
        self.text = text
        self.children = []
        self.parent = parent

    def __repr__(self):
        return repr(self.text)


class Element:
    def __init__(self, tag, attributes, parent):
        self.tag = tag
        self.attributes = attributes
        self.children = []
        self.parent = parent

    def __repr__(self):
        return "<" + self.tag + ">"


SELF_CLOSING_TAGS = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
]


class HTMLParser:
    def __init__(self, body):
        self.body = body
        self.unfinished = []

    def parse(self):
        root = Element("html", {}, None)
        self.unfinished = [root]

        text = ""
        in_tag = False

        for c in self.body:
            if c == "<":
                in_tag = True
                if text:
                    self.add_text(text)
                text = ""
            elif c == ">":
                in_tag = False
                self.add_tag(text)
                text = ""
            else:
                text += c

        if text and not in_tag:
            self.add_text(text)

        return root

    def add_text(self, text):
        if text.isspace():
            return
        parent = self.unfinished[-1]
        parent.children.append(Text(text, parent))

    def add_tag(self, tag):
        tag, attributes = self.get_attributes(tag)

        if tag.startswith("!"):
            return

        if tag.startswith("/"):
            if len(self.unfinished) == 1:
                return
            node = self.unfinished.pop()
            self.unfinished[-1].children.append(node)
            return

        if tag in SELF_CLOSING_TAGS:
            parent = self.unfinished[-1]
            parent.children.append(Element(tag, attributes, parent))
            return

        parent = self.unfinished[-1]
        node = Element(tag, attributes, parent)
        self.unfinished.append(node)

    def get_attributes(self, text):
        parts = text.split()
        tag = parts[0].casefold()
        attributes = {}

        for attr in parts[1:]:
            if "=" in attr:
                key, value = attr.split("=", 1)
                value = value.strip("\"'")
                attributes[key.casefold()] = value
            else:
                attributes[attr.casefold()] = ""

        return tag, attributes

    def print_tree(node, indent=0):
        print(" " * indent + repr(node))
        for child in node.children:
            HTMLParser.print_tree(child, indent + 2)


