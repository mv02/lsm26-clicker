import os
from typing import Callable
import pygame as pg
from pygame.typing import ColorLike

from crafting import Recipe


CONTROL_BTN_SIZE = 60
CONTROL_BTN_PADDING = 8

UPGRADE_BTN_WIDTH = 400
UPGRADE_BTN_HEIGHT = 100
UPGRADE_BTN_PADDING = 10


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
        self.rect = pg.Rect(x, y, CONTROL_BTN_SIZE, CONTROL_BTN_SIZE)
        self.callback = callback

        # Load the icon and compute its size
        self.icon = pg.image.load(os.path.join("assets", "fa", f"{icon_name}.svg"))
        icon_size = CONTROL_BTN_SIZE - 2 * CONTROL_BTN_PADDING

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
            border_radius=int(CONTROL_BTN_SIZE / 2),
        )

        screen.blit(
            self.icon,
            (
                self.rect.x + CONTROL_BTN_PADDING,
                self.rect.y + CONTROL_BTN_PADDING,
                CONTROL_BTN_SIZE,
                CONTROL_BTN_SIZE,
            ),
        )


class UpgradeButton:
    def __init__(
        self,
        x: float,
        y: float,
        recipe: Recipe,
        bg_color: ColorLike,
        text_color: ColorLike,
        callback: Callable,
    ):
        self.rect = pg.Rect(x, y, UPGRADE_BTN_WIDTH, UPGRADE_BTN_HEIGHT)
        self.callback = callback
        self.recipe = recipe

        self.heading_font = pg.font.SysFont("Arial", 24, True)
        self.font = pg.font.SysFont("Arial", 16)

        # Load and resize the image
        # TODO: custom images
        self.image = pg.image.load(os.path.join("assets", "placeholder.svg"))
        self.image = pg.transform.scale(self.image, (self.rect.h, self.rect.h))
        size = UPGRADE_BTN_HEIGHT

        # Create a mask with alpha channel
        mask = pg.Surface((size, size), pg.SRCALPHA)
        mask.fill((0, 0, 0, 0))

        pg.draw.rect(
            mask,
            (255, 255, 255, 255),
            (0, 0, size, size),
            border_top_left_radius=10,
            border_bottom_left_radius=10,
        )

        # Round the image corners by blending with the mask
        rounded_image = pg.Surface((size, size), pg.SRCALPHA)
        rounded_image.blit(self.image)
        rounded_image.blit(mask, special_flags=pg.BLEND_RGBA_MIN)
        self.image = rounded_image

        self.bg_color = pg.Color(bg_color)
        self.text_color = pg.Color(text_color)
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
            border_radius=10,
        )

        screen.blit(self.image, (self.rect.x, self.rect.y, self.rect.h, self.rect.h))

        text_x = self.rect.x + UPGRADE_BTN_HEIGHT + UPGRADE_BTN_PADDING
        text_y = self.rect.y + UPGRADE_BTN_PADDING

        # Draw recipe name
        text = self.heading_font.render(self.recipe.name, True, self.text_color)
        screen.blit(text, (text_x, text_y))

        # Draw recipe description
        text = self.font.render(self.recipe.description, True, self.text_color)
        screen.blit(text, (text_x, text_y + 55))
