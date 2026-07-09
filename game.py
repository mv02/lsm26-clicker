from crafting import Recipe


class Game:
    def __init__(self):
        self.points = 0.0
        self.points_per_click = 1
        # TODO: click multiplier
        self.points_per_second = 0.0
        self.inventory = []

    def click(self):
        self.points += 1
        # TODO: random drops

    def passive_points(self):
        self.points += self.points_per_second / 60

    def available_upgrades(self) -> list[Recipe]:
        # TODO: return craftable items
        return []

    def buy_upgrade(self, item_name: str):
        # TODO: handle upgrade purchase/item crafting
        print(f"Purchased {item_name}")

    # TODO: upgrades, inventory
