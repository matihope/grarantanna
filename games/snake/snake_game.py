from modules import \
    basic_classes, \
    basic_globals, \
    game_class

from games.snake import snake_player
from games.snake import snake_fruit


class SnakeGame(game_class.Game):
    def __init__(self, width, height, fps=60):
        super().__init__(width, height, fps)
        self.bg_color = (50, 50, 50)
        self.snake = snake_player.SnakePlayer(size=50)
        self.add_updatable(self.snake)

        self.fruit = snake_fruit.Fruit(size=50)
        self.add_drawable(self.fruit)
        self.fruit.kill()
        self.snake_score = 0

    def update(self):
        super().update()

        if self.snake.x == self.fruit.x and self.snake.y == self.fruit.y:
            self.fruit.kill()
            self.snake_score += 1
            self.snake.grow()

