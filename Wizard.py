import arcade
from models import World
import math

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 600


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()


class BurnWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.score = 0
        self.wizard_sprite = ModelSprite('images/Wizard.png', model=self.world.player)
        self.start_game = ModelSprite('images/Start.jpg', model=self.world.start_game)
        self.end = ModelSprite('images/End.jpg', model=self.world.end)
        self.help_button = False
        self.background = ModelSprite('images/RealBack_1.jpg', model=self.world.background)
        self.heart = ModelSprite('images/heart.png', model=self.world.heart_life)
        self.another_heart = ModelSprite('images/heart.png', model=self.world.another_heart)
        self.fire_1 = ModelSprite('images/fire.png', model=self.world.fire_1)
        self.fire_2 = ModelSprite('images/fire.png', model=self.world.fire_2)
        self.fire_3 = ModelSprite('images/fire.png', model=self.world.fire_3)
        self.another_fire = ModelSprite('images/fire.png', model=self.world.another_fire)
        self.bonus = ModelSprite('images/Bonus.png', model=self.world.bonus)
        self.bonus_1 = ModelSprite('images/Bonus_1.png', model=self.world.bonus_1)
        self.bonus_2 = ModelSprite('images/Bonus_2.png', model=self.world.bonus_2)
        self.zombie = ModelSprite('images/Zombie.png', model=self.world.zombie)
        self.grim = ModelSprite('images/Ghost_1.png', model=self.world.grim)
        self.ghost = ModelSprite('images/Ghost_2.png', model=self.world.ghost)
        self.witch = ModelSprite('images/Witch.png', model=self.world.witch)
        self.TinkerBell = ModelSprite('images/Tinker_Bell.png', model=self.world.TinkerBell)
        self.Ariel = ModelSprite('images/Royal_3.png', model=self.world.Ariel)
        self.help = ModelSprite('images/Help.jpg', model=self.world.help)

    def update(self, delta):
        self.world.update(delta)

    def on_draw(self):
        arcade.start_render()
        if self.world.state == 2:
            self.background.draw()
            self.heart.draw()
            arcade.draw_text(str(self.world.life), 300, 550, arcade.color.BLACK, 20)
            self.wizard_sprite.draw()
            self.score = f"Level {self.world.level} : {str(self.world.score) } / {str(self.world.score_reach)}"
            arcade.draw_text(str(self.score), 20, 550, arcade.color.BLACK, 20)
            if self.world.level >= 3 and self.world.fire_1.stat == [True, False, False]:
                self.world.another_fire.stat = True
                self.another_fire.draw()
            if self.world.level >= 7 and self.world.fire_1.stat == [True, True, False]:
                self.world.another_fire.stat = True
                self.another_fire.draw()
            if self.world.life >= 9:
                self.world.another_heart.stat = False
            else:
                self.another_heart.draw()
            if self.world.fire_1.stat[0]:
                self.fire_1.draw()
                if self.world.fire_1.stat[1]:
                    self.fire_2.draw()
                    if self.world.fire_1.stat[2]:
                        self.fire_3.draw()
            if self.world.bonus_stat:
                self.bonus_2.draw()
                arcade.draw_text(str(math.ceil(self.world.bonus_time)), 440, 550, arcade.color.BLACK, 20)
            else:
                self.bonus_1.draw()
            self.bonus.draw()
            self.zombie.draw()
            self.grim.draw()
            self.ghost.draw()
            self.witch.draw()
            self.TinkerBell.draw()
            self.Ariel.draw()
        elif self.world.state == 3:
            self.end.draw()
            arcade.draw_text("Your score: " + str(self.world.score), 220, 345, arcade.color.BLACK, 20, align="center",
                             anchor_x="center", anchor_y="center")
        else:
            self.start_game.draw()
            if self.help_button:
                self.help.draw()

    def on_key_press(self, key, key_modifiers):
        if not self.world.is_started() and key == arcade.key.ENTER:
            self.world.start()
        if self.help_button is not True and key == arcade.key.F1:
            self.help_button = True
        if self.help_button and key == arcade.key.ESCAPE:
            self.help_button = False
        self.world.reset_on_key_press(key, key_modifiers)
        self.world.fire_on_key_press(key, key_modifiers)
        self.world.player_on_key_press(key, key_modifiers)


def main():
    window = BurnWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
