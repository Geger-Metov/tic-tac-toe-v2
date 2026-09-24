from app.domain.service.game_interface import IGameService
from app.domain.model.game import Game
from app.domain.model.board import Board
from app.datasource.repository.game_repository import GameRepo

from uuid import UUID

class GameService(IGameService):
    HUMAN_SYMBOL = 1
    COMPUTER_SYMBOL = -1
    WIN_SCORE = 10
    DRAW_SCORE = 0

    def __init__(self, repo : GameRepo) -> None:
        self._repo = repo

    def get_next_move(self, game: Game) -> Game:
        board = game.board
        best_score = float('-inf')
        best_move = None

        # Перебираем все пустые клетки (возможные ходы компьютера)
        for i in range(3):
            for j in range(3):
                if board.get_cell(i, j) == 0:
                    # Создаём копию доски и делаем ход компьютера
                    new_board = self._copy_board(board)
                    new_board.grid[i][j] = self.COMPUTER_SYMBOL

                    # Вызываем минимакс для оценки этого хода (следующим ходит человек => минимизирующий)
                    score = self._minimax(new_board, 0, False)

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        # Если best_move не назначен (доска полная), возвращаем исходную игру
        if best_move is None:
            return game

        # Применяем лучший ход и создаём новую игру
        final_board = self._copy_board(board)
        final_board.grid[best_move[0]][best_move[1]] = self.COMPUTER_SYMBOL
        updated_game = Game(id=game.id, board=final_board)
        self._repo.save(updated_game)
        return updated_game
    
    def validate_field(self, old_game: Game, new_game: Game) -> bool:
        if old_game.id != new_game.id:
            return False
        
        changes = 0
        for i in range(3):
            for j in range(3):
                old_cell =  old_game.board.get_cell(i, j)
                new_cell = new_game.board.get_cell(i, j)
                if old_cell != new_cell:
                    changes += 1
                    if not (old_cell == 0 and new_cell == 1):
                        return False
        return changes == 1
    
    def is_game_over(self, game: Game) -> bool:
        winner = self._check_winner(game.board)
        if winner != 0:
            return True
        return not game.board.has_empty_cells()

    def _check_winner(self, board: Board) -> int:
        """Возвращает 1 (победа X), -1 (победа O) или 0 (нет победителя)."""
        lines = []
        for i in range(3):
            lines.append([board.get_cell(i, j) for j in range(3)])
            lines.append([board.get_cell(j, i) for j in range(3)])
        lines.append([board.get_cell(i, i) for i in range(3)])
        lines.append([board.get_cell(i, 2 - i) for i in range(3)])

        for line in lines:
            if line[0] != 0 and line[0] == line[1] == line[2]:
                return line[0]
        return 0

    def _minimax(self, board: Board, depth: int, is_maximizing: bool) -> int:
        """
        :param board: текущая доска
        :param depth: глубина рекурсии (необязательно, но полезно для предпочтения быстрых побед)
        :param is_maximizing: True, если ход компьютера (максимизирующего игрока),
                              False, если ход человека (минимизирующего)
        :return: оценка позиции (с точки зрения компьютера)
        """
        # Проверяем терминальное состояние
        winner = self._check_winner(board)
        if winner == self.COMPUTER_SYMBOL:
            return self.WIN_SCORE - depth   # быстрая победа предпочтительнее
        elif winner == self.HUMAN_SYMBOL:
            return -self.WIN_SCORE + depth  # оттягиваем поражение
        elif not board.has_empty_cells():
            return self.DRAW_SCORE

        if is_maximizing:
            best = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board.get_cell(i, j) == 0:
                        new_board = self._copy_board(board)
                        new_board.grid[i][j] = self.COMPUTER_SYMBOL
                        score = self._minimax(new_board, depth + 1, False)
                        best = max(best, score)
            return int(best)
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board.get_cell(i, j) == 0:
                        new_board = self._copy_board(board)
                        new_board.grid[i][j] = self.HUMAN_SYMBOL
                        score = self._minimax(new_board, depth + 1, True)
                        best = min(best, score)
            return int(best)

    def _copy_board(self, board: Board) -> Board:
        new_grid = [row[:] for row in board.grid]
        return Board(grid=new_grid)
    
    def get_game_by_id(self, id: UUID) -> Game:
        game = self._repo.find_by_id(id)
        if game is None:
            raise ValueError(f"Game with id {id} not found")
        return game

    def process_user_move_and_computer_response(self, user_game: Game) -> Game:
        self._repo.save(user_game)
        if self.is_game_over(user_game):
            return user_game
        updated_game = self.get_next_move(user_game)
        return updated_game
    
    def save_game(self, game: Game) -> None:
        self._repo.save(game)
