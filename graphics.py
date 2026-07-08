import pygame as pg
from pygame.typing import Point

from components import ControlButton, BTN_SIZE


CLICKER_SIZE = 100

HEADER_HEIGHT = 120
HEADER_COLOR = "black"
BUTTONS_MARGIN = 20
BUTTONS_SPACING = 20
SCORE_COLOR = "white"

FOOTER_HEIGHT = 50
FOOTER_COLOR = "black"
FOOTER_TEXT_COLOR = "white"
FOOTER_TEXT_MARGIN = 10


class Graphics:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Load and resize the clicker sprite
        # TODO: custom image
        self.clicker_image = pg.image.load("assets/placeholder.svg")
        self.clicker_image = pg.transform.scale(
            self.clicker_image, (CLICKER_SIZE, CLICKER_SIZE)
        )

        self.clicker_growing = False
        self.clicker_animation = 0

        # Initialize and load fonts
        pg.font.init()
        self.score_font = pg.font.SysFont("Arial", 72, True)
        self.footer_font = pg.font.SysFont("Arial", 18)

        # Create control buttons
        btn_y = BUTTONS_MARGIN
        btn_x = self.width - BUTTONS_MARGIN - BTN_SIZE
        quit_button = ControlButton(
            btn_x,
            btn_y,
            "xmark-solid-full",
            "#c72300",
            "white",
            lambda: pg.event.post(pg.Event(pg.QUIT)),
        )
        btn_x -= BUTTONS_SPACING + BTN_SIZE
        # TODO: audio button handler
        audio_button = ControlButton(
            btn_x, btn_y, "volume-solid-full", "#004cff", "white", lambda: None
        )
        btn_x -= BUTTONS_SPACING + BTN_SIZE
        # TODO: save button handler
        save_button = ControlButton(
            btn_x, btn_y, "floppy-disk-solid-full", "#004cff", "white", lambda: None
        )
        self.buttons = [save_button, audio_button, quit_button]

        self.draw_background()
        self.draw_footer()
        self.draw_clicker()

    def draw_background(self):
        # TODO: background images
        self.screen.fill("gray")

    def draw_header(self):
        pg.draw.rect(self.screen, HEADER_COLOR, (0, 0, self.width, HEADER_HEIGHT))

        # Draw all buttons
        for button in self.buttons:
            button.draw(self.screen)

    def draw_score(self, points: float):
        text = self.score_font.render(str(round(points)), True, SCORE_COLOR)
        coords = (
            self.width / 2 - text.get_width() / 2,
            HEADER_HEIGHT / 2 - text.get_height() / 2,
        )
        self.screen.blit(text, coords)

    def draw_footer(self):
        footer = pg.draw.rect(
            self.screen,
            FOOTER_COLOR,
            (0, self.height - FOOTER_HEIGHT, self.width, FOOTER_HEIGHT),
        )

        text = self.footer_font.render("LSM 2026", True, FOOTER_TEXT_COLOR)
        coords = (
            footer.x + FOOTER_TEXT_MARGIN,
            self.height - FOOTER_TEXT_MARGIN - text.get_height(),
        )
        self.screen.blit(text, coords)

    def draw_clicker(self):
        # Advance the animation
        if self.clicker_growing:
            self.clicker_animation += 5
            if self.clicker_animation >= 20:
                self.clicker_growing = False
        else:
            self.clicker_animation = max(self.clicker_animation - 5, 0)

        size = CLICKER_SIZE * (1 + self.clicker_animation / 100)
        self.clicker_image = pg.transform.scale(self.clicker_image, (size, size))
        coords = (
            (self.width - self.clicker_image.width) / 2,
            (self.height - self.clicker_image.height) / 2,
        )
        self.clicker = self.screen.blit(self.clicker_image, coords)

    def is_in_clicker(self, pos: Point):
        return self.clicker.collidepoint(pos)
