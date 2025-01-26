from collections import deque, namedtuple
import random


class TypeDish(namedtuple):
    name: str
    category: str
    price: int

    def __lt__(self, other):
        return self.price < other.price

menu = [
    ('Pizza', 'Main', 10),
    ('Spaghetti', 'Main', 8),
    ('Steak', 'Main', 15),
]
type_menu = [TypeDish(*v) for v in menu]
sorted(type_menu)


class MenuPicker:
    def __init__(self, menu):
        self.menu = menu
        # 最新の3日分の履歴のみを保持する！
        self.history = deque(maxlen=3)

    def pick(self):
        while True:
            choice = random.choice(self.menu)
            if choice not in self.history:
                break
        self.history.append(choice)
        return choice
