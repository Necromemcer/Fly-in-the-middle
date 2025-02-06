import time
import pygame
import random
import sys

class FlyGame:
    def __init__(self, grid_size, move_interval):
        self.grid_size = grid_size
        self.move_interval = move_interval  # milliseconds
        self.moves = []
        pygame.init()
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
    #
    def generate_random_path(self):
        n = self.grid_size
        P = random.randint(5, 15)  # Random path length between 7 and 10
        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        directions_names = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        # Set the starting point at the middle of the grid
        start_x, start_y = n // 2, n // 2
        path = [(start_x, start_y)]
        moves = []
        # Generate the path
        while len(path) < P:
            x, y = path[-1]  # Current cell
            possible_moves = []
            # Check all possible directions
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n:  # Ensure the move is within the grid
                    possible_moves.append((dx, dy))
            # Randomly choose a valid move
            dx, dy = random.choice(possible_moves)
            next_x, next_y = x + dx, y + dy
            path.append((next_x, next_y))
            moves.append(directions_names[directions.index((dx, dy))])
        # Ensure the path finishes near the edge of the grid
        def ensure_to_finish_on_the_edge(x, y):
            # Calculate the distance to the nearest edge
            distance_to_edge = min(x, n - 1 - x, y, n - 1 - y)
            # If already near the edge, return the current position
            if distance_to_edge == 0:
                return x, y
            # Move toward the nearest edge
            if x == distance_to_edge:
                return x - 1, y  # Move left
            elif n - 1 - x == distance_to_edge:
                return x + 1, y  # Move right
            elif y == distance_to_edge:
                return x, y - 1  # Move up
            else:
                return x, y + 1  # Move down
        # Ensure the final position is near the edge
        x, y = path[-1]
        if min(x, n - 1 - x, y, n - 1 - y) > 0:  # If not already near the edge
            next_x, next_y = ensure_to_finish_on_the_edge(x, y)
            dx, dy = next_x - x, next_y - y
            path.append((next_x, next_y))
            moves.append(directions_names[directions.index((dx, dy))])
        # Add a critical (impossible) move at the end of the sequence
        x, y = path[-1]  # Current cell
        impossible_moves = []
        # Check all impossible directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < n and 0 <= ny < n):  # Ensure the move is outside the grid
                impossible_moves.append((dx, dy))
        # Randomly choose an invalid move
        dx, dy = random.choice(impossible_moves)
        moves.append(directions_names[directions.index((dx, dy))])
        return moves
    #
    def main_loop(self):
        running = True
        sequence_index = 0
        last_time = pygame.time.get_ticks()
        game_over = False  # Track if the game is over
        reaction_time = 0  # Track the player's reaction time
        critical_move_shown = False  # Track if the critical move has been shown
        player_lost = False  # Track if the player lost by pressing space too early
        #
        # Initialize the display
        screen_width, screen_height = 700, 700
        self.display = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Fly Game")
        #
        # Generate the random path
        self.moves = self.generate_random_path()
        #
        # Countdown before the game starts
        countdown_values = [f"FLY IN THE MIDDLE {self.grid_size} by {self.grid_size}", "REACT BY PRESSING 'SPACE'", "3", "2", "1", "START"]
        for text in countdown_values:
            self.display.fill((255, 255, 255))  # White background
            countdown_text = self.font.render(text, True, (0, 0, 0))
            # Center the text
            text_rect = countdown_text.get_rect(center=(screen_width // 2, screen_height // 2))
            self.display.blit(countdown_text, text_rect)
            pygame.display.flip()
            pygame.time.wait(1800)
        #
        # Main game loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if not critical_move_shown:
                        # Player pressed space before the critical move was shown
                        player_lost = True
                        game_over = True
                    else:
                        # Player pressed space after the critical move was shown
                        reaction_time = (pygame.time.get_ticks() - last_time) / 1000
                        game_over = True
            # Render moves sequentially with timed intervals
            current_time = pygame.time.get_ticks()
            if not game_over and current_time - last_time >= self.move_interval:
                if sequence_index < len(self.moves):
                    # Display the current move
                    move_text = self.moves[sequence_index]
                    print(f"Move: {move_text}")
                    self.display.fill((255, 255, 255))  # White background
                    move_display = self.font.render(move_text, True, (0, 0, 0))
                    text_rect = move_display.get_rect(center=(screen_width // 2, screen_height // 2))
                    self.display.blit(move_display, text_rect)
                    pygame.display.flip()
                    # Check if this is the critical move
                    if sequence_index == len(self.moves) - 1:
                        critical_move_shown = True
                        last_time = pygame.time.get_ticks()  # Reset timer for reaction time
                    sequence_index += 1
                    last_time = current_time
                else:
                    # All moves have been shown
                    game_over = True
            #
            # Handle game over state
            if game_over:
                self.display.fill((255, 255, 255))  # White background
                if player_lost:
                    result_text = self.font.render("YOU'VE LOST DUE TO PREMATURE REACTION.", True, (255, 0, 0))
                else:
                    result_text = self.font.render(f"REACTION TIME: {reaction_time:.3f} SECONDS", True, (0, 0, 0))
                text_rect = result_text.get_rect(center=(screen_width // 2, screen_height // 2))
                self.display.blit(result_text, text_rect)
                pygame.display.flip()
                # Wait for a few seconds before closing the game
                pygame.time.wait(3000)
                running = False
            self.clock.tick(60)
        pygame.quit()

print("Choose the size of grid (3, 5):")
size = int(input())
print("Choose the time interval [milliseconds] (1000/1500/2000, etc.):")
interval = int(input())

game = FlyGame(size, interval)
game.main_loop()