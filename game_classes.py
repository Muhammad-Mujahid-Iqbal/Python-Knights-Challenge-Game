from enum import Enum


class KnightStatus(Enum):
    LIVE = "LIVE"
    DEAD = "DEAD"
    DROWNED = "DROWNED"


class Knight:
    def __init__(self, name, symbol):
        self.attack = 1
        self.defence = 1
        self.item = None
        self.name = name
        self.status = KnightStatus.LIVE.value
        self.symbol = symbol
        self.last_location = 'n/a'

    def get_attack(self):
        if self.item:
            return self.attack + self.item.attack
        return self.attack

    def get_defence(self):
        if self.item:
            return self.defence + self.item.defence
        return self.defence

    def __repr__(self):
        return "KNIGHT: " + self.name


class GameMove:
    def __init__(self, knight_symbol, direction):
        self.knight_symbol = knight_symbol
        self.direction = direction

    def __repr__(self):
        return "{}:{}".format(self.knight_symbol, self.direction)


class Item:
    def __init__(self, name, attack=0, defence=0, symbol=None):
        self.attack = attack
        self.defence = defence
        self.name = name
        self.equipped = False
        self.symbol = symbol

    def __repr__(self):
        return self.name


class Cell:
    def __init__(self, knight=None, item=None):
        self.knight = knight
        self.items = []
        if item:
            self.items.append(item)

    def __repr__(self):
        symbol = self.knight.symbol if self.knight else ''
        items = [item.symbol for item in self.items] if self.items else ''
        return "{} {}".format(symbol, items)


class Arena:
    def __init__(self):
        self.board = [[Cell() for _ in range(8)] for _ in range(8)]

        self.red_knight = Knight('RED', 'R')
        self.blue_knight = Knight('BLUE', 'B')
        self.green_knight = Knight('GREEN', 'G')
        self.yellow_knight = Knight('YELLOW', 'Y')

        self.axe = Item('axe', attack=2, symbol='A')
        self.dagger = Item('dagger', attack=1, symbol='D')
        self.helmet = Item('helmet', defence=1, symbol='H')
        self.magic_staff = Item('magic_staff', attack=1, defence=1, symbol='M')

    def place_knights(self):
        self.board[0][0] = Cell(knight=self.red_knight)
        self.board[7][0] = Cell(knight=self.blue_knight)
        self.board[7][7] = Cell(knight=self.green_knight)
        self.board[0][7] = Cell(knight=self.yellow_knight)

    def place_items(self):
        self.board[2][2] = Cell(item=self.axe)
        self.board[2][5] = Cell(item=self.dagger)
        self.board[5][5] = Cell(item=self.helmet)
        self.board[5][2] = Cell(item=self.magic_staff)

    def print_arena_state(self):
        for row in self.board:
            print(row)
        print('')

    def get_knight_from_arena(self, knight_symbol):
        for row in range(8):
            for col in range(8):
                cell = self.board[row][col]
                if cell.knight is not None and cell.knight.symbol == knight_symbol:
                    return cell.knight, (row, col)
        return None, None

    def get_item_from_arena(self, item_symbol):
        for row in range(8):
            for col in range(8):
                cell = self.board[row][col]
                for item in cell.items:
                    if item.symbol == item_symbol:
                        return (row, col)
        return None
