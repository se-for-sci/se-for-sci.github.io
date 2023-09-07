import nox


@nox.session
def run(session):
    session.install("textual")
    session.run("python", "textual_example.py")
