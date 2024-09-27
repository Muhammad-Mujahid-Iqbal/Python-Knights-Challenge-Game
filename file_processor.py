from game_classes import GameMove


class FileProcessor:
    file_path = 'moves.txt'

    @staticmethod
    def read_game_file():
        """
        Generator function to read the game file line by line.
        This function yields each line after stripping any leading/trailing whitespace.
        """
        with open(FileProcessor.file_path, 'r') as file:
            for line in file:
                yield line.strip()

    @staticmethod
    def validate_move_format(move):
        """
        Validate that each move is in the correct format (X:Y)
        """
        if len(move) != 3 or move[1] != ':':
            return False
        if not move[2].isupper() or not move[0].isupper():
            return False

        valid_knight_letters = ('R', 'B', 'G', 'Y')
        valid_directions = ('N', 'E', 'S', 'W')

        if move[0] not in valid_knight_letters or move[2] not in valid_directions:
            return False

        return True

    @staticmethod
    def process_game_file():
        """
        Method to process game file. It reads the file, validates the moves and returns them to game
        """

        game_moves = FileProcessor.read_game_file()
        moves = []

        try:
            first_line = next(game_moves)
            if first_line != "GAME-START":
                raise ValueError("Invalid file format: Missing 'GAME-START' in beginning")

            for move in game_moves:
                if move == "GAME-END":
                    return moves
                if FileProcessor.validate_move_format(move):
                    moves.append(
                        GameMove(knight_symbol=move[0], direction=move[2])
                    )
                else:
                    raise ValueError(f"Invalid move encountered: {move}")
            raise ValueError("Invalid file format: It is missing 'GAME-END'")

        except StopIteration:
            raise ValueError("Invalid file format: File ended Unexpectedly!!!")
