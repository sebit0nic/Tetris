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
        self.rotation = random.choice(range(len(game.block_list[self.name])))  # DONE randomize rotation (e.g. 0, 1, 2, 3; Hint: different number of rotations per block)
        self.set_shape(game.block_list[self.name][self.rotation])
        self.x = int(game.board_width / 2) - int(self.width / 2)
        self.y = 0
        self.color = game.block_colors[block_name]  # DONE Set Color correctly / Can be 'red', 'green', ... (see self.blockColors)

    def set_shape(self, shape):
        self.shape = shape
        self.height = 0
        self.width = 0
        for shape_row in shape:
            shape_column_count = 0
            self.height += 1  # DONE Calculate the correct height
            for shape_column in shape_row:
                if shape_column == 'x':
                    shape_column_count += 1
            if shape_column_count > self.width:
                self.width = shape_column_count  # DONE Calculate the correct width

    def right_rotation(self, rotation_options):
        # DONE rotate block once clockwise
        self.rotation += 1
        if self.rotation > len(rotation_options) - 1:
            self.rotation = 0
        self.set_shape(rotation_options[self.rotation])
        pass

    def left_rotation(self, rotation_options):
        # DONE rotate block once counter-clockwise
        self.rotation -= 1
        if self.rotation < 0:
            self.rotation = len(rotation_options) - 1
        self.set_shape(rotation_options[self.rotation])
        pass

    def move_downwards(self, game):
        self.y += game.speed/5

    def move_sideways(self, direction):
        self.x += direction

class Game(BaseGame):
    def run_game(self):
        self.board = self.get_empty_board()
        fall_time = time.time()

        current_block = self.get_new_block()
        next_block = self.get_new_block()

        # TODO Fill in the score dictionary
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
            self.test_quit_game()
            # TODO Game Logic: implement key events & move blocks (Hint: check if move is valid/block is on the Board)
            current_key = self.check_key_press()
            if current_key == pygame.K_LEFT:
                print('Left Key pressed')
                if self.is_block_on_valid_position(current_block, -1, 0):
                    current_block.move_sideways(-1)
            if current_key == pygame.K_RIGHT:
                print('Right Key pressed')
                if self.is_block_on_valid_position(current_block, 1, 0):
                    current_block.move_sideways(1)
            if current_key == pygame.K_DOWN:
                print('Down Key pressed')
            if current_key == pygame.K_q:
                print('Q Key pressed')
                current_block.left_rotation(self.block_list[current_block.name])
            if current_key == pygame.K_e:
                print('E Key pressed')
                current_block.right_rotation(self.block_list[current_block.name])
            if current_key == pygame.K_p:
                print('P Key pressed')
                self.set_game_speed(0)

            #if self.is_block_on_valid_position(current_block, 0, self.speed/5):
            #    current_block.move_downwards(self)
            #else:
            #    self.add_block_to_board(current_block)

            #print(self.board)

            # Draw after game logic
            self.display.fill(self.background)
            self.draw_game_board()
            self.draw_score()
            self.draw_next_block(next_block)
            if current_block != None:
                self.draw_block(current_block)
            pygame.display.update()
            self.set_game_speed(self.speed)
            self.clock.tick(self.speed)

    # Check if Coordinate given is on board (returns True/False)
    def is_coordinate_on_board(self, x, y):
        # TODO check if coordinate is on playingboard (in boundary of self.boardWidth and self.boardHeight)
        if x < 0 or x > self.board_width:
            return False
        if y < 0 or y > self.board_height:
            return False
        return True

    # Parameters block, x_change (any movement done in X direction), yChange (movement in Y direction)
    # Returns True if no part of the block is outside the Board or collides with another Block
    def is_block_on_valid_position(self, block, x_change=0, y_change=0):
        # TODO check if block is on valid position after change in x or y direction
        if block.x + x_change < 0 or block.x + block.width + x_change > self.board_width:
            return False
        if block.y + block.height + y_change < 0 or block.y + block.height + y_change > self.board_height:
            return False
        return True

    # Check if the line on y Coordinate is complete
    # Returns True if the line is complete
    def check_line_complete(self, y_coord):
        # TODO check if line on yCoord is complete and can be removed
        return False

    # Go over all lines and remove those, which are complete
    # Returns Number of complete lines removed
    def remove_complete_line(self):
        # TODO go over all lines and check if one can be removed
        return 0

    # Create a new random block
    # Returns the newly created Block Class
    def get_new_block(self):
        # DONE make block choice random! (Use random.choice out of the list of blocks) see blocknames array
        blockname = random.choice(Block.blocknames)
        block = Block(self, blockname)
        return block

    def add_block_to_board(self, block):
        # TODO once block is not falling, place it on the gameboard
        #  add Block to the designated Location on the board once it stopped moving
        # Block zu self.board hinzufügen
        self.board[int(block.y)][int(block.x)] = 'x'

    # calculate new Score after a line has been removed
    def calculate_new_score(self, lines_removed, level):
        # TODO calculate new score
        # Points gained: Points per line removed at once times the level modifier!
        # Points per lines removed corresponds to the score_directory
        # The level modifier is 1 higher than the current level.
        pass

    # calculate new Level after the score has changed
        # TODO calculate new level
    def calculate_new_level(self, score):
        # The level generally corresponds to the score divided by 300 points.
        # 300 -> level 1; 600 -> level 2; 900 -> level 3
        # TODO increase gamespeed by 1 on level up only
        pass

    # set the current game speed
    def set_game_speed(self, speed):
        # TODO set the correct game speed!
        self.speed = speed
        pass

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
