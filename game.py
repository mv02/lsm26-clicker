class Game:
    def __init__(self):
        self.points = 0.0
        self.points_per_second = 0.0
        self.inventory = []

    def click(self):
        self.points += 1
        # TODO: random drops

    def passive_points(self):
        self.points += self.points_per_second / 60

    # TODO: upgrades, inventory
