# Tetris - DYOA Advanced at TU Graz WS 2020
# Name:       Sebastian Lackner
# Student ID: 12005098

import pygame, sys, time, random
from pygame.locals import *
from framework import BaseGame


# Recommended Start: init function of Block Class
class Block:
    blocknames = ['clevelandZ', 'rhodeIslandZ', 'blueRicky', 'smashBoy', 'orangeRicky', 'teewee', 'hero']

    def __init__(self, game, block_name):
        self.name = block_name  # DONE set name / Can be 'hero', 'teewee', ...
        self.rotation = random.choice(range(len(game.block_list[self.name])))  # randomize rotation (e.g. 0, 1, 2, 3)
        self.set_shape(game.block_list[self.name][self.rotation])
        self.x = int(game.board_width / 2) - int(self.width / 2)
        self.y = 0
        self.color = game.block_colors[block_name]  # Set Color correctly (see self.blockColors)

    # Set a particular shape from the block_list
    def set_shape(self, shape):
        self.shape = shape
        self.height = 0
        self.width = 0
        # Go through each row of the given shape inside the block_list
        for shape_row in shape:
            self.height += 1  # DONE Calculate the correct height
            shape_column_count = len(shape_row)
            # Only set width of the block if it is the largest width yet (otherwise a smaller value might overwrite
            # the previous one
            if shape_column_count > self.width:
                self.width = shape_column_count  # DONE Calculate the correct width

    def right_rotation(self, rotation_options):
        # DONE rotate block once clockwise
        self.rotation += 1
        # If rotation has been increased to something bigger than the list allows, set it back to 0
        if self.rotation > len(rotation_options) - 1:
            self.rotation = 0
        self.set_shape(rotation_options[self.rotation])

    def left_rotation(self, rotation_options):
        # DONE rotate block once counter-clockwise
        self.rotation -= 1
        # If rotation has been decreased to something lower than 0, set it back the list length
        if self.rotation < 0:
            self.rotation = len(rotation_options) - 1
        self.set_shape(rotation_options[self.rotation])

    # Move block downwards by one position
    def move_downwards(self, game):
        self.y += 1

    # Move block left or right
    def move_sideways(self, direction):
        self.x += direction


class Game(BaseGame):
    level = 0
    speed_up = False

    def run_game(self):
        self.gameboard = self.get_empty_board()

        current_block = self.get_new_block()
        next_block = self.get_new_block()
        game_over = False

        # DONE Fill in the score dictionary
        #  Maps "lines removed" to "raw points gained"
        #  0 lines: 0 points; 1 line: 40 points; 2 lines: 100 points; 3 lines: 300 points; 4 lines: 1200 points
        self.score_dictionary = {
            0: 0,
            1: 40,
            2: 100,
            3: 300,
            4: 1200
        }

        # GameLoop
        while True:
            self.evaluate_key_press(current_block)

            # Check if block is on valid position after moving downwards and if not, add the block to the gameboard
            # also check if lines are completed and spawn new block
            if self.is_block_on_valid_position(current_block, 0, 1):
                current_block.move_downwards(self)
            else:
                self.add_block_to_board(current_block)
                if current_block.y - current_block.height <= 0:
                    game_over = True
                self.remove_complete_line()
                current_block = next_block
                next_block = self.get_new_block()

            # Draw after game logic
            self.display.fill(self.background)
            self.draw_game_board()
            self.draw_score()
            # Also added textbox for the level
            self.draw_level()
            self.draw_next_block(next_block)
            if current_block != None:
                self.draw_block(current_block)

            # Check if we are in a gameover state and if yes, exit game loop
            if game_over:
                break
            pygame.display.update()
            self.set_game_speed(self.speed)

            # Check if player is pressing K_DOWN so that blocks are falling faster
            if self.speed_up:
                self.clock.tick(self.speed + 2)
            else:
                self.clock.tick(self.speed)

    # Function to check for each key press (KEYUP and KEYDOWN events!)
    def evaluate_key_press(self, current_block):
        self.test_quit_game()
        for event in pygame.event.get([KEYDOWN, KEYUP]):
            if event.type == KEYDOWN:
                if event.key == pygame.K_p:
                    self.show_text('Paused')

                # For left and right movement, check if block is on valid position after moving it and if not, move it
                # back to initial position
                if event.key == pygame.K_LEFT:
                    if self.is_block_on_valid_position(current_block, -1, 0):
                        current_block.move_sideways(-1)
                if event.key == pygame.K_RIGHT:
                    if self.is_block_on_valid_position(current_block, 1, 0):
                        current_block.move_sideways(1)

                # For left and right rotation, check if block is on valid position after rotating it and if not,
                # rotate it back to initial position
                if event.key == pygame.K_q:
                    current_block.left_rotation(self.block_list[current_block.name])
                    if not self.is_block_on_valid_position(current_block):
                        current_block.right_rotation(self.block_list[current_block.name])
                if event.key == pygame.K_e:
                    current_block.right_rotation(self.block_list[current_block.name])
                    if not self.is_block_on_valid_position(current_block):
                        current_block.left_rotation(self.block_list[current_block.name])

                if event.key == pygame.K_DOWN:
                    self.speed_up = True

            if event.type == KEYUP:
                if event.key == pygame.K_DOWN:
                    self.speed_up = False

    # Check if Coordinate given is on board (returns True/False)
    def is_coordinate_on_board(self, x, y):
        # DONE check if coordinate is on playingboard (in boundary of self.boardWidth and self.boardHeight)
        if x < 0 or x > self.board_width - 1:
            return False
        if y < 0 or y > self.board_height - 1:
            return False
        return True

    # Parameters block, x_change (any movement done in X direction), yChange (movement in Y direction)
    # Returns True if no part of the block is outside the Board or collides with another Block
    # DONE check if block is on valid position after change in x or y direction
    def is_block_on_valid_position(self, block, x_change=0, y_change=0):
        # First, check if each cell inside a block is still on a valid y position
        for shape_y_idx in range(block.height):
            if block.y + shape_y_idx + y_change > self.board_height - 1:
                return False

            # Then, check for each cell inside a block is still on a valid x position
            for shape_x_idx in range(block.width):
                if block.x + shape_x_idx + x_change > self.board_width - 1 or block.x + shape_x_idx + x_change < 0:
                    return False

                # Lastly, check if cells inside a block collide with other blocks already on the gameboard
                if block.shape[shape_y_idx][shape_x_idx] != '.':
                    if self.gameboard[block.y + shape_y_idx + y_change][block.x + shape_x_idx + x_change] != '.':
                        return False

        return True

    # Check if the line on y Coordinate is complete
    # Returns True if the line is complete
    def check_line_complete(self, y_coord):
        blocks_on_coord = 0
        # Check on the given y position of the gameboard how many blocks are currently there
        for board_x_idx in self.gameboard[y_coord]:
            if board_x_idx != '.':
                blocks_on_coord += 1

        # If the count of how many block are on the y position matches the board width, return true
        if blocks_on_coord == self.board_width:
            return True

        return False

    # Go over all lines and remove those, which are complete
    # Returns Number of complete lines removed
    def remove_complete_line(self):
        # DONE go over all lines and check if one can be removed
        total_removed_lines = 0
        # Go through each y position on the gameboard and check if the line is complete
        for board_y_idx in range(len(self.gameboard)):
            if self.check_line_complete(board_y_idx):
                total_removed_lines += 1

                # If line is completed, go through each line backwards bottom to top starting from the current y
                for board_row_idx in range(board_y_idx, 0, -1):
                    for board_column_idx in range(len(self.gameboard[board_row_idx])):
                        # Replace the current cell with the cell that's right above it
                        self.gameboard[board_row_idx][board_column_idx] = self.gameboard[board_row_idx-1][board_column_idx]

        self.calculate_new_score(total_removed_lines, self.level)

    # Create a new random block
    # Returns the newly created Block Class
    def get_new_block(self):
        # DONE make block choice random! (Use random.choice out of the list of blocks) see blocknames array
        blockname = random.choice(Block.blocknames)
        block = Block(self, blockname)
        return block

    def add_block_to_board(self, block):
        # DONE once block is not falling, place it on the gameboard
        #  add Block to the designated Location on the board once it stopped moving
        for shape_y_idx in range(block.height):
            for shape_x_idx in range(block.width):
                # Go through each cell of the block and if it is solid, add it to the gameboard by transforming the
                # cell position to board position
                if block.shape[shape_y_idx][shape_x_idx] == 'x':
                    self.gameboard[block.y + shape_y_idx][block.x + shape_x_idx] = block.color

    # calculate new Score after a line has been removed
    def calculate_new_score(self, lines_removed, level):
        # DONE calculate new score
        # Points gained: Points per line removed at once times the level modifier!
        # Points per lines removed corresponds to the score_directory
        # The level modifier is 1 higher than the current level.
        self.score += self.score_dictionary[lines_removed] * (level + 1)
        self.calculate_new_level(self.score)

    # calculate new Level after the score has changed
        # DONE calculate new level
    def calculate_new_level(self, score):
        # The level generally corresponds to the score divided by 300 points.
        # 300 -> level 1; 600 -> level 2; 900 -> level 3
        # DONE increase gamespeed by 1 on level up only
        self.level = int(score / 300)
        self.speed = 5 + self.level

    # set the current game speed
    def set_game_speed(self, speed):
        # DONE set the correct game speed!
        self.speed = speed

# -------------------------------------------------------------------------------------
# Do not modify the code below, your implementation should be done above
# -------------------------------------------------------------------------------------


def main():
    pygame.init()
    game = Game()

    game.display = pygame.display.set_mode((game.window_width, game.window_height))
    game.clock = pygame.time.Clock()
    pygame.display.set_caption('Tetris')

    game.show_text('Tetris')

    game.run_game()
    game.show_text('Game Over')


if __name__ == '__main__':
    main()
