#!/usr/bin/env python

from textual.app import App, ComposeResult
from textual.widgets import Static, Header, Footer, Input


class PrincetonApp(App):
    """Displays the Princeton colors."""

    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Input(placeholder="Name")
        for color in ["black", "orange"] * 2:
            stripe = Static()
            stripe.styles.height = "1fr"
            stripe.styles.background = color
            yield stripe
        yield Footer()


if __name__ == "__main__":
    PrincetonApp().run()
