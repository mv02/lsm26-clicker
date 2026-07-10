import os
import pygame as pg

from game import Game
from graphics import Graphics

# Initialize pygame
pg.init()

# Create the screen and clock
screen = pg.display.set_mode(flags=pg.FULLSCREEN)
clock = pg.time.Clock()

running = True

game = Game()
gfx = Graphics(screen)

game.load_game()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            # Exit the game
            running = False

        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            # Escape
            running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            # Mouse click
            if event.button == pg.BUTTON_LEFT and gfx.is_in_clicker(event.pos):
                game.click()
                gfx.clicker_growing = True

        elif event.type == pg.USEREVENT:
            # Upgrade event
            game.buy_upgrade(event.item_name)

        elif event.type == pg.USEREVENT + 1:
            # Save event
            game.save_game()

        # Send events to buttons
        for button in gfx.buttons():
            button.handle_event(event)

    game.passive_points()

    gfx.draw_background()
    gfx.draw_header()
    gfx.draw_score(game.points)
    gfx.draw_clicker()
    gfx.draw_footer()
    gfx.draw_left_sidebar(game.available_upgrades(), game.inventory)
    gfx.draw_right_sidebar(game.points_per_click, game.points_per_second, [])
    pg.display.flip()

    clock.tick(60)

pg.quit()
