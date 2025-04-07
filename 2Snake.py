import pygame
import random
import time

pygame.init()

# 屏幕尺寸
width, height = 600, 400
cell_size = 20
grid_width = width // cell_size
grid_height = height // cell_size

# 颜色
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# 字体
font = pygame.font.SysFont("Arial", 24)

# 方向定义
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

# 食物类：包含位置、分数、生成时间
class Food:
    def __init__(self, snake):
        while True:
            self.position = (
                random.randint(0, grid_width - 1),
                random.randint(0, grid_height - 1)
            )
            if self.position not in snake:
                break
        self.weight = random.choice([1, 2, 5])  # 随机选择权重
        self.spawn_time = time.time()  # 记录食物生成的时间

    def is_expired(self):
        return time.time() - self.spawn_time > 5  # 5 秒后食物消失

    def draw(self):
        x, y = self.position
        color = red if self.weight == 1 else yellow if self.weight == 2 else white
        pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

class SnakeGame:
    def __init__(self):
        self.snake = [(5, 5)]
        self.direction = right
        self.foods = [Food(self.snake)]  # 食物列表
        self.score = 0
        self.level = 1
        self.speed = 7
        self.max_speed = 20
        self.running = True

    def move(self):
        """移动蛇身并处理逻辑"""
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # 撞墙或撞到自己
        if (new_head in self.snake or
                new_head[0] < 0 or new_head[0] >= grid_width or
                new_head[1] < 0 or new_head[1] >= grid_height):
            self.running = False
            return

        self.snake.insert(0, new_head)

        # 检查是否吃到食物
        eaten = False
        for food in self.foods:
            if food.position == new_head:
                self.score += food.weight
                eaten = True
                self.foods.remove(food)
                # 每 5 分升级一次
                if self.score % 5 == 0:
                    self.level += 1
                    self.speed = min(self.speed + 2, self.max_speed)
                break

        if not eaten:
            self.snake.pop()

        # 移除过期的食物
        self.foods = [food for food in self.foods if not food.is_expired()]

        # 有一定几率生成新食物
        if len(self.foods) < 3 and random.random() < 0.05:
            self.foods.append(Food(self.snake))

    def draw(self):
        """绘制游戏场景"""
        screen.fill(black)

        # 画蛇
        for x, y in self.snake:
            pygame.draw.rect(screen, green, (x * cell_size, y * cell_size, cell_size, cell_size))

        # 画食物
        for food in self.foods:
            food.draw()

        # 显示分数和等级
        score_text = font.render(f"Score: {self.score}  Level: {self.level}", True, white)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def handle_events(self):
        """处理按键事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != down:
                    self.direction = up
                elif event.key == pygame.K_DOWN and self.direction != up:
                    self.direction = down
                elif event.key == pygame.K_LEFT and self.direction != right:
                    self.direction = left
                elif event.key == pygame.K_RIGHT and self.direction != left:
                    self.direction = right

if __name__ == "__main__":
    game = SnakeGame()
    clock = pygame.time.Clock()

    while game.running:
        clock.tick(game.speed)
        game.handle_events()
        game.move()
        game.draw()

    pygame.quit()
