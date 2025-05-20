import random

# Grid and snake setup
grid_size = 10
snake = [(0, 0)]
direction_map = {"W": (-1, 0), "A": (0, -1), "S": (1, 0), "D": (0, 1)}

def draw_grid(snake, food):
    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) in snake:
                print("S", end=" ")
            elif (i, j) == food:
                print("F", end=" ")
            else:
                print(".", end=" ")
        print()

def generate_food(snake):
    while True:
        food = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        if food not in snake:
            return food

food = generate_food(snake)

# Game loop
while True:
    draw_grid(snake, food)
    move = input("Move (W/A/S/D): ").upper()
    if move not in direction_map:
        print("Invalid move. Try again.")
        continue

    # Calculate new head position
    head = snake[-1]
    delta = direction_map[move]
    new_head = (head[0] + delta[0], head[1] + delta[1])

    # Check collision
    if (
        new_head[0] < 0 or new_head[0] >= grid_size or
        new_head[1] < 0 or new_head[1] >= grid_size or
        new_head in snake
    ):
        print("Game Over! You hit something.")
        break

    # Grow or move
    if new_head == food:
        snake.append(new_head)
        food = generate_food(snake)
    else:
        snake.append(new_head)
        snake.pop(0)
