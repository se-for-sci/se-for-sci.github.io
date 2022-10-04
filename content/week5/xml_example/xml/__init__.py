import functools


class XML:
    def __init__(self, *content, **attributes):
        self.content = content
        self.attributes = attributes

    @property
    def name(self):
        return self.__class__.__name__.lower()

    def __str__(self):
        attributes = "".join(f' {k}="{v}"' for k, v in self.attributes.items())
        if self.content:
            content = " ".join(str(c) for c in self.content)
            return f"<{self.name}{attributes}>{content}</{self.name}>\n"
        return f"<{self.name}{attributes}/>"


@functools.cache
def __getattr__(name):
    return type(name, (XML,), {})
