import os
from typing import Callable
import pygame as pg

from pygame.typing import ColorLike


BTN_SIZE = 60
BTN_PADDING = 8


class ControlButton:
    def __init__(
        self,
        x: float,
        y: float,
        icon_name: str,
        bg_color: ColorLike,
        icon_color: ColorLike,
        callback: Callable,
    ):
        self.rect = pg.Rect(x, y, BTN_SIZE, BTN_SIZE)
        self.callback = callback

        # Load the icon and compute its size
        self.icon = pg.image.load(os.path.join("assets", "fa", f"{icon_name}.svg"))
        icon_size = BTN_SIZE - 2 * BTN_PADDING

        # Resize and recolor the icon
        self.icon = pg.transform.scale(self.icon, (icon_size, icon_size))
        self.icon = pg.transform.solid_overlay(self.icon, icon_color)

        self.bg_color = pg.Color(bg_color)
        self.icon_color = pg.Color(icon_color)
        self.is_hovered = False

    def handle_event(self, event: pg.Event):
        if event.type == pg.MOUSEMOTION:
            # Check if hovered
            was_hovered = self.is_hovered
            self.is_hovered = self.rect.collidepoint(event.pos)
            # Set the cursor
            if self.is_hovered and not was_hovered:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            elif not self.is_hovered and was_hovered:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        elif (
            event.type == pg.MOUSEBUTTONDOWN
            and event.button == pg.BUTTON_LEFT
            and self.rect.collidepoint(event.pos)
        ):
            # Left click
            self.callback()

    def draw(self, screen: pg.Surface):
        pg.draw.rect(
            screen,
            self.bg_color if not self.is_hovered else self.bg_color.correct_gamma(2),
            self.rect,
            border_radius=int(BTN_SIZE / 2),
        )

        screen.blit(
            self.icon,
            (self.rect.x + BTN_PADDING, self.rect.y + BTN_PADDING, BTN_SIZE, BTN_SIZE),
        )
