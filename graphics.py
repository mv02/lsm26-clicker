import pygame as pg
from pygame.typing import Point

from components import (
    ControlButton,
    CONTROL_BTN_SIZE,
    UPGRADE_BTN_HEIGHT,
    UpgradeButton,
)
from crafting import Recipe


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

SIDEBAR_WIDTH = 400
SIDEBAR_MARGIN = 40
SIDEBAR_PADDING = 40
SIDEBAR_BORDER_RADIUS = 20
SIDEBAR_COLOR = "darkgray"
SIDEBAR_TEXT_COLOR = "black"


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
        self.sidebar_heading_font = pg.font.SysFont("Arial", 32, True)
        self.sidebar_font = pg.font.SysFont("Arial", 24)

        # Create control buttons
        btn_y = BUTTONS_MARGIN
        btn_x = self.width - BUTTONS_MARGIN - CONTROL_BTN_SIZE
        quit_button = ControlButton(
            btn_x,
            btn_y,
            "xmark-solid-full",
            "#c72300",
            "white",
            lambda: pg.event.post(pg.Event(pg.QUIT)),
        )
        btn_x -= BUTTONS_SPACING + CONTROL_BTN_SIZE
        # TODO: audio button handler
        audio_button = ControlButton(
            btn_x, btn_y, "volume-solid-full", "#004cff", "white", lambda: None
        )
        btn_x -= BUTTONS_SPACING + CONTROL_BTN_SIZE
        # TODO: save button handler
        save_button = ControlButton(
            btn_x, btn_y, "floppy-disk-solid-full", "#004cff", "white", lambda: None
        )
        self.control_buttons = [save_button, audio_button, quit_button]
        self.upgrade_buttons: list[UpgradeButton] = []

    def draw_background(self):
        # TODO: background images
        self.screen.fill("gray")

    def draw_header(self):
        pg.draw.rect(self.screen, HEADER_COLOR, (0, 0, self.width, HEADER_HEIGHT))

        # Draw all buttons
        for button in self.control_buttons:
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

    def draw_left_sidebar(self, upgrades: list[Recipe], inventory: list[str]):
        # Create upgrade buttons
        self.upgrade_buttons = [
            UpgradeButton(
                SIDEBAR_MARGIN,
                HEADER_HEIGHT
                + SIDEBAR_MARGIN
                + i * (BUTTONS_SPACING + UPGRADE_BTN_HEIGHT),
                recipe,
                SIDEBAR_COLOR,
                SIDEBAR_TEXT_COLOR,
                lambda r=recipe: pg.event.post(
                    pg.Event(pg.USEREVENT, item_name=r.name)
                ),
            )
            for i, recipe in enumerate(upgrades)
        ]

        # Draw all buttons
        for button in self.upgrade_buttons:
            button.draw(self.screen)

        # Draw inventory
        # TODO: better inventory
        inventory_height = (
            self.height
            - HEADER_HEIGHT
            - FOOTER_HEIGHT
            - 2 * SIDEBAR_MARGIN
            - len(upgrades) * (BUTTONS_SPACING + UPGRADE_BTN_HEIGHT)
        )
        inventory_rect = pg.draw.rect(
            self.screen,
            SIDEBAR_COLOR,
            (
                SIDEBAR_MARGIN,
                HEADER_HEIGHT
                + SIDEBAR_MARGIN
                + len(upgrades) * (BUTTONS_SPACING + UPGRADE_BTN_HEIGHT),
                SIDEBAR_WIDTH,
                inventory_height,
            ),
            border_radius=10,
        )

        text_x = inventory_rect.x + SIDEBAR_PADDING
        text_y = inventory_rect.y + SIDEBAR_PADDING

        text = self.sidebar_heading_font.render("Inventory", True, SIDEBAR_TEXT_COLOR)
        self.screen.blit(text, (text_x, text_y))

        for i, item in enumerate(inventory):
            text = self.sidebar_font.render(item, True, SIDEBAR_TEXT_COLOR)
            self.screen.blit(text, (text_x, text_y + 60 + i * 40))

    def draw_right_sidebar(
        self, points_per_click: int, points_per_second: float, equipment: list[str]
    ):
        coords = (
            self.width - SIDEBAR_MARGIN - SIDEBAR_WIDTH,
            HEADER_HEIGHT + SIDEBAR_MARGIN,
        )
        dimensions = (
            SIDEBAR_WIDTH,
            self.height - HEADER_HEIGHT - FOOTER_HEIGHT - 2 * SIDEBAR_MARGIN,
        )

        self.right_sidebar = pg.draw.rect(
            self.screen,
            SIDEBAR_COLOR,
            coords + dimensions,
            border_radius=SIDEBAR_BORDER_RADIUS,
        )

        text_x = self.right_sidebar.x + SIDEBAR_PADDING
        text_y = self.right_sidebar.y + SIDEBAR_PADDING

        lines = {
            # Stats heading
            0: self.sidebar_heading_font.render("Stats", True, SIDEBAR_TEXT_COLOR),
            # Points per click
            60: self.sidebar_font.render(
                f"{points_per_click} points/click", True, SIDEBAR_TEXT_COLOR
            ),
            # Points per second
            100: self.sidebar_font.render(
                f"{points_per_second} points/s", True, SIDEBAR_TEXT_COLOR
            ),
            # Equipment heading
            160: self.sidebar_heading_font.render(
                "Equipment", True, SIDEBAR_TEXT_COLOR
            ),
            # TODO: draw upgrades/equipment
        }

        # Draw every line of text
        for y, text_line in lines.items():
            self.screen.blit(text_line, (text_x, text_y + y))

    def buttons(self):
        return self.control_buttons + self.upgrade_buttons
