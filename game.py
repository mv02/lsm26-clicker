import os
from crafting import Recipe


SAVE_FILE_PATH = "save.txt"


class Game:
    def __init__(self):
        self.points = 0.0
        self.points_per_click = 1
        # TODO: click multiplier
        self.points_per_second = 0.0
        self.inventory = []
        self.upgrades: list[Recipe] = []

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

    def save_game(self):
        with open(SAVE_FILE_PATH, "w") as f:
            f.write(f"{self.points} {self.points_per_click} {self.points_per_second}\n")
            f.write("\n")

            for upgrade in self.upgrades:
                f.write(upgrade.name + "\n")
            f.write("\n")

            for item in self.inventory:
                f.write(item + "\n")

    def load_game(self):
        if not os.path.exists(SAVE_FILE_PATH):
            return

        with open(SAVE_FILE_PATH) as f:
            # First line
            p, ppc, pps = f.readline().split()
            self.points = float(p)
            self.points_per_click = int(ppc)
            self.points_per_second = float(pps)

            # Empty line
            f.readline()

            # Upgrades and empty line
            for line in f:
                if line.strip() == "":
                    break
                # TODO: load upgrades
                print("upgrade " + line.strip())

            # Inventory
            for line in f:
                # TODO: load inventory
                print("item " + line.strip())
