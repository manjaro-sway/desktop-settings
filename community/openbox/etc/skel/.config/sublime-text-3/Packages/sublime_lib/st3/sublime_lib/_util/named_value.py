class NamedValue():
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return self.name
