import pygame
import random
import time
import psycopg2

# PostgreSQL database connection
conn = psycopg2.connect(dbname="postgres", user="postgres", password="0419")
cur = conn.cursor()

pygame.init()

# Screen dimensions
width, height = 600, 400
cell_size = 20
grid_width = width // cell_size
grid_height = height // cell_size

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Font
font = pygame.font.SysFont("Arial", 24)

# Directions
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

# Food class: Position, weight, spawn time
class Food:
    def __init__(self, snake):
        while True:
            self.position = (
                random.randint(0, grid_width - 1),
                random.randint(0, grid_height - 1)
            )
            if self.position not in snake:
                break
        self.weight = random.choice([1, 2, 5])  # Random weight
        self.spawn_time = time.time()  # Time food was spawned

    def is_expired(self):
        return time.time() - self.spawn_time > 5  # Food expires after 5 seconds

    def draw(self):
        x, y = self.position
        color = red if self.weight == 1 else yellow if self.weight == 2 else white
        pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

# Snake Game Class
class SnakeGame:
    def __init__(self):
        self.snake = [(5, 5)]
        self.direction = right
        self.foods = [Food(self.snake)]  # List of foods
        self.score = 0
        self.level = 1
        self.speed = 7
        self.max_speed = 20
        self.running = True

    def move(self):
        """Move the snake and handle logic"""
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Check if the snake hits a wall or itself
        if (new_head in self.snake or
                new_head[0] < 0 or new_head[0] >= grid_width or
                new_head[1] < 0 or new_head[1] >= grid_height):
            self.running = False
            return

        self.snake.insert(0, new_head)

        # Check if the snake eats food
        eaten = False
        for food in self.foods:
            if food.position == new_head:
                self.score += food.weight
                eaten = True
                self.foods.remove(food)
                # Level up every 5 points
                if self.score % 5 == 0:
                    self.level += 1
                    self.speed = min(self.speed + 2, self.max_speed)
                break

        if not eaten:
            self.snake.pop()

        # Remove expired food
        self.foods = [food for food in self.foods if not food.is_expired()]

        # Occasionally spawn new food
        if len(self.foods) < 3 and random.random() < 0.05:
            self.foods.append(Food(self.snake))

    def draw(self):
        """Draw the game scene"""
        screen.fill(black)

        # Draw the snake
        for x, y in self.snake:
            pygame.draw.rect(screen, green, (x * cell_size, y * cell_size, cell_size, cell_size))

        # Draw the food
        for food in self.foods:
            food.draw()

        # Display score and level
        score_text = font.render(f"Score: {self.score}  Level: {self.level}", True, white)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def handle_events(self):
        """Handle keyboard events"""
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

def add_user(username):
    """Add user to 'users' table"""
    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
    user_id = cur.fetchone()[0]  # Get the inserted user_id
    conn.commit()
    return user_id

def add_score(username, score):
    """Add score for user"""
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cur.fetchone()

    if user_id is None:
        # User doesn't exist, add the user
        user_id = add_user(username)
        print(f"User {username} added with level 1.")
    else:
        user_id = user_id[0]  # Get the existing user_id

    # Insert score into the user_score table
    cur.execute("INSERT INTO user_score (user_id, score) VALUES (%s, %s)",
                (user_id, score))
    conn.commit()
    print(f"Score for {username} added: {score}")

def get_user_score(username):
    """Fetch the user's latest score"""
    cur.execute("SELECT score FROM user_score WHERE user_id = (SELECT id FROM users WHERE username = %s) ORDER BY id DESC LIMIT 1", (username,))
    score = cur.fetchone()
    if score:
        return score[0]
    return None

if __name__ == "__main__":
    # Get username input from the user
    username = input("Enter your username: ")

    # Initialize the game
    game = SnakeGame()
    clock = pygame.time.Clock()

    # Check if user exists in database and fetch score
    user_score = get_user_score(username)
    if user_score is not None:
        print(f"Welcome back {username}! Your last score was: {user_score}")
    else:
        print(f"Hello {username}, no previous scores found.")

    while game.running:
        clock.tick(game.speed)
        game.handle_events()
        game.move()
        game.draw()

    # After the game ends, add the score to the database
    add_score(username, game.score)
    pygame.quit()
