class Episode:
    def __init__(self, title: str, description: str = None):
        self.title = title
        self.description = description if description is not None else None
