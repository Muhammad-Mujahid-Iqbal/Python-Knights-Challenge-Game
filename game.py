import json

from file_processor import FileProcessor
from game_classes import Arena, Cell, Item, Knight, KnightStatus


class BattlingKnight:
    def __init__(self):
        self.arena = Arena()
        self.arena.place_knights()
        self.arena.place_items()
        self.moves = None
        self.direction_map = {
            'N': (-1, 0),
            'S': (1, 0),
            'E': (0, 1),
            'W': (0, -1)
        }

    def make_knight_drown(self, knight, original_location):
        """
        Method to make given knight in drown state, leave any item
        """
        original_cell: Cell = self.arena.board[original_location[0]][original_location[1]]
        knight.status = KnightStatus.DROWNED.value
        knight.attack = 0
        knight.defence = 0
        if knight.item:
            item = knight.item
            item.equipped = False
            original_cell.items.append(item)
            knight.item = None
        original_cell.knight = None
        knight.last_location = None

    def make_knight_dead(self, knight, location):
        """
        Method to make given knight as dead and give up any item if available
        """
        cell: Cell = self.arena.board[location[0]][location[1]]
        knight.status = KnightStatus.DEAD.value
        knight.attack = 0
        knight.defence = 0
        if knight.item:
            item = knight.item
            item.equipped = False
            cell.items.append(item)
            knight.item = None
        knight.last_location = location

    @staticmethod
    def pick_item_by_priority(items):
        """
        Method for returning an item from given items based on priority (A M D H)
        """

        priority_order = {'A': 1, 'M': 2, 'D': 3, 'H': 4}
        highest_priority_item = min(
            items,
            key=lambda item: priority_order.get(item.symbol, float('inf'))
        )

        return highest_priority_item

    def play_move_in_arena(self, move):
        """
        Core method to play a knight's move on board
        """
        knight_to_move: Knight
        location: tuple
        knight_to_move, location = self.arena.get_knight_from_arena(move.knight_symbol)

        # play only if knight is alive
        if not knight_to_move or knight_to_move.status is not KnightStatus.LIVE.value:
            return

        # create new location to move knight
        dx, dy = self.direction_map[move.direction]
        new_location = (location[0] + dx, location[1] + dy)

        # check for drowning
        if not (0 <= new_location[0] <= 7) or not (0 <= new_location[1] <= 7):
            self.make_knight_drown(knight=knight_to_move, original_location=location)
            return

        target_cell: Cell = self.arena.board[new_location[0]][new_location[1]]

        # check if next location has items
        if target_cell.items:
            # if knight already has item, skip
            if knight_to_move.item is None:
                item: Item = self.pick_item_by_priority(target_cell.items)
                item.equipped = True
                knight_to_move.item = item
                target_cell.items.remove(item)

        # fight if there is another knight, else just move
        if target_cell.knight:
            attacker: Knight = knight_to_move
            defender: Knight = target_cell.knight

            attacker_attack_score = attacker.get_attack()
            defender_defence_score = defender.get_defence()

            # add element of surprise score
            attacker_attack_score += 0.5

            if attacker_attack_score > defender_defence_score:
                # attacker wins
                self.make_knight_dead(knight=defender, location=new_location)
                target_cell.knight = attacker
            else:
                # defender wins
                self.make_knight_dead(knight=attacker, location=new_location)
                target_cell.knight = defender
        else:
            target_cell.knight = knight_to_move

        # remove knight from previous cell
        previous_cell = self.arena.board[location[0]][location[1]]
        previous_cell.knight = None

    def play_game(self):
        self.arena.print_arena_state()
        for move in self.moves:
            print('Move', move)
            self.play_move_in_arena(move)
            self.arena.print_arena_state()

    @staticmethod
    def write_to_json_file(results):
        with open('final_state.json', 'w') as json_file:
            json_file.write('{\n')
            for idx, (key, value) in enumerate(results.items()):
                json_file.write(f' "{key}": {json.dumps(value, separators=(",", ":"))}')
                if idx < len(results) - 1:
                    json_file.write(",\n")
                else:
                    json_file.write("\n")
            json_file.write('}\n')

        print('Saved Results to JSON')

    def save_results_to_json(self):
        """
        Method to save state of game in JSON format
        """
        red_knight = self.arena.red_knight
        blue_knight = self.arena.blue_knight
        yellow_knight = self.arena.yellow_knight
        green_knight = self.arena.green_knight
        magic_staff = self.arena.magic_staff
        helmet = self.arena.helmet
        dagger = self.arena.dagger
        axe = self.arena.axe

        locations = {
            'red': red_knight.last_location,
            'green': green_knight.last_location,
            'yellow': yellow_knight.last_location,
            'blue': blue_knight.last_location,
            'magic_staff': self.arena.get_item_from_arena('M'),
            'helmet': self.arena.get_item_from_arena('H'),
            'dagger': self.arena.get_item_from_arena('D'),
            'axe': self.arena.get_item_from_arena('A')
        }

        location_update_dict = {'red': 'R', 'green': 'G', 'yellow': 'Y', 'blue': 'B'}
        for key, value in location_update_dict.items():
            if locations[key] == 'n/a':
                # get live location for knights who are alive, update item location as well if they carry
                knight, locations[key] = self.arena.get_knight_from_arena(value)
                if knight.item:
                    locations[knight.item.name] = locations[key]

        result = {
            "red": [
                list(locations['red']) if locations['red'] else None,
                red_knight.status,
                red_knight.item.name if red_knight.item else None,
                red_knight.get_attack(),
                red_knight.get_defence()
            ],
            "blue": [
                list(locations['blue']) if locations['blue'] else None,
                blue_knight.status,
                blue_knight.item.name if blue_knight.item else None,
                blue_knight.get_attack(),
                blue_knight.get_defence()
            ],
            "green": [
                list(locations['green']) if locations['green'] else None,
                green_knight.status,
                green_knight.item.name if green_knight.item else None,
                green_knight.get_attack(),
                green_knight.get_defence()
            ],
            "yellow": [
                list(locations['yellow']) if locations['yellow'] else None,
                yellow_knight.status,
                yellow_knight.item.name if yellow_knight.item else None,
                yellow_knight.get_attack(),
                yellow_knight.get_defence()
            ],
            "magic_staff": [
                list(locations['magic_staff']) if locations['magic_staff'] else None,
                magic_staff.equipped
            ],
            "helmet": [
                list(locations['helmet']) if locations['helmet'] else None,
                helmet.equipped
            ],
            "dagger": [
                list(locations['dagger']) if locations['dagger'] else None,
                dagger.equipped
            ],
            "axe": [
                list(locations['axe']) if locations['axe'] else None,
                axe.equipped
            ]
        }

        self.write_to_json_file(results=result)

    def read_moves_from_file(self):
        try:
            self.moves = FileProcessor.process_game_file()
        except ValueError as e:
            self.moves = None
            print(e)
            print("Terminating Game!")


if __name__ == "__main__":
    game = BattlingKnight()
    game.read_moves_from_file()
    if game.moves:
        game.play_game()
        game.save_results_to_json()
