import arcade.key
from random import randint
import sys

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4

DIR_OFFSETS = {DIR_STILL: (0, 0),
               DIR_UP: (0, 1),
               DIR_DOWN: (0, -1)}

KEY_MAP = {arcade.key.UP: DIR_UP,
           arcade.key.DOWN: DIR_DOWN, }

MOVEMENT_SPEED = 5

Freeze = 0

DIR_OFFSET = {DIR_RIGHT: (10, 0),
              DIR_LEFT: (-10, 0),
              Freeze: (0, 0)}


def is_hit_fire(self, world, r_x, r_y, fire_number):
    if self.x - r_x <= self.world.fire_1.x <= self.x + r_x and self.y - r_y <= self.world.fire_1.y <= self.y + r_y and \
            self.world.fire_1.x != 150 or \
            self.x - r_x <= self.world.fire_2.x <= self.x + r_x and self.y - r_y <= self.world.fire_2.y <= self.y + r_y and \
            self.world.fire_2.x != 150 or \
            self.x - r_x <= self.world.fire_3.x <= self.x + r_x and self.y - r_y <= self.world.fire_3.y <= self.y + r_y and \
            self.world.fire_3.x != 150:
        arcade.sound.play_sound(world.hit_sound)
        if fire_number == 1:
            world.fire_1.fire = False
            world.fire_1.fire_set()
        elif fire_number == 2:
            world.fire_2.fire = False
            world.fire_2.fire_set()
        elif fire_number == 3:
            world.fire_3.fire = False
            world.fire_3.fire_set()
        world.score += self.score
        self.stat = False
        self.come_back()


class Decoration:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 10


class Player:
    GRAVITY = 1
    STARTING_VELOCITY = 15
    JUMPING_VELOCITY = 15

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vy = 0
        self.stat = True

    def update(self, delta):
        if self.stat:
            self.y += self.vy
            self.vy -= Player.GRAVITY
            if self.y <= 130:
                self.y = 130

    def jump(self):
        self.vy = Player.JUMPING_VELOCITY

    def reset(self):
        self.x = 80
        self.y = 130
        self.stat = True


class Fire:
    FIRE_SPEED = 20

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 0
        self.number = 1
        self.fire = True
        self.stat = [True, False, False]

    def update(self, delta):
        if self.fire:
            if self.x <= self.world.width and self.vx != 0:
                self.x += self.vx
            else:
                self.fire_set()

    def attack(self):
        self.vx = Fire.FIRE_SPEED

    def fire_set(self):
        self.fire = True
        self.x = 150
        self.y = self.world.player.y
        self.vx = 0

    def reset(self):
        self.fire_set()
        self.stat = [True, False, False]


class Zombie:
    GRAVITY = 1
    STARTING_VELOCITY = 12
    JUMPING_VELOCITY = 12

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 5
        self.vy = Zombie.STARTING_VELOCITY
        self.vyy = Zombie.STARTING_VELOCITY
        self.score = 30
        self.stat = True

    def update(self, delta):
        if self.stat:
            self.y += self.vy
            self.vy -= Zombie.GRAVITY
            self.x -= 5
            if self.y <= 130:
                self.y = 130
                self.vy = self.vyy
            if self.x <= 0:
                self.come_back()
                self.world.life -= 1
        else:
            self.x = 0
            self.y = 0

    def jump(self):
        self.vy = Player.JUMPING_VELOCITY

    def hit(self):
        is_hit_fire(self, self.world, 20, 90, 1)
        is_hit_fire(self, self.world, 20, 90, 2)
        is_hit_fire(self, self.world, 20, 90, 3)

    def come_back(self):
        self.stat = True
        self.x = 2000
        self.y = 130

    def reset(self):
        self.come_back()
        self.vx = 5
        self.vy = Zombie.STARTING_VELOCITY
        self.vyy = Zombie.STARTING_VELOCITY


class Grim:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 10
        self.score = 40
        self.stat = True

    def update(self, delta):
        if self.stat:
            if self.x <= 0:
                self.come_back()
                self.world.life -= 1
            else:
                self.x -= self.vx
        else:
            self.x = 0
            self.y = 0

    def hit(self):
        is_hit_fire(self, self.world, 20, 80, 1)
        is_hit_fire(self, self.world, 20, 80, 2)
        is_hit_fire(self, self.world, 20, 80, 3)

    def come_back(self):
        self.stat = True
        self.x = 2500
        self.y = 130

    def reset(self):
        self.come_back()
        self.vx = 10


class Ghost:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 8
        self.score = 20
        self.stat = True

    def update(self, delta):
        if self.stat:
            if self.x <= 0:
                self.come_back()
                self.world.life -= 1
            else:
                self.x -= self.vx
        else:
            self.x = 0
            self.y = 0

    def hit(self):
        is_hit_fire(self, self.world, 20, 80, 1)
        is_hit_fire(self, self.world, 20, 80, 2)
        is_hit_fire(self, self.world, 20, 80, 3)

    def come_back(self):
        self.stat = True
        self.x = 3500
        self.y = randint(300, 500)

    def reset(self):
        self.come_back()
        self.vx = 8


class Witch:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 8
        self.score = 20
        self.stat = True

    def update(self, delta):
        if self.stat:
            if self.x <= 0:
                self.come_back()
                self.world.life -= 1
            else:
                self.x -= self.vx
        else:
            self.x = 0
            self.y = 0

    def hit(self):
        is_hit_fire(self, self.world, 20, 80, 1)
        is_hit_fire(self, self.world, 20, 80, 2)
        is_hit_fire(self, self.world, 20, 80, 3)

    def come_back(self):
        self.stat = True
        self.x = 4500
        self.y = randint(300, 500)

    def reset(self):
        self.come_back()
        self.vx = 8


class TinkerBell:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 8
        self.score = 20
        self.stat = True

    def update(self, delta):
        if self.stat:
            if self.x <= 0:
                self.come_back()
            else:
                self.x -= self.vx
        else:
            self.x = 0
            self.y = 0

    def hit(self):
        is_hit_fire(self, self.world, 20, 80, 1)
        is_hit_fire(self, self.world, 20, 80, 2)
        is_hit_fire(self, self.world, 20, 80, 3)

    def come_back(self):
        self.stat = True
        self.x = 6500
        self.y = randint(300, 500)

    def reset(self):
        self.come_back()
        self.vx = 8


class Ariel:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 8
        self.score = 20
        self.stat = True

    def update(self, delta):
        if self.stat:
            if self.x <= 0:
                self.come_back()
            else:
                self.x -= self.vx
        else:
            self.x = 0
            self.y = 0

    def hit(self):
        is_hit_fire(self, self.world, 20, 80, 1)
        is_hit_fire(self, self.world, 20, 80, 2)
        is_hit_fire(self, self.world, 20, 80, 3)

    def come_back(self):
        self.stat = True
        self.x = 7500
        self.y = 130

    def reset(self):
        self.come_back()
        self.vx = 8


class AnotherFire:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 10
        self.stat = False

    def update(self, delta):
        if self.stat:
            if self.x <= 0:
                self.come_back()
            else:
                self.x -= self.vx

    def hit(self):
        if self.x - 20 <= self.world.player.x <= self.x + 20 and self.y - 50 <= self.world.player.y <= self.y + 50:
            self.world.fire_1.number += 1
            self.x = 2000
            self.y = randint(200, 540)
            self.stat = False
            if self.world.fire_1.stat == [True, False, False]:
                self.world.fire_1.stat = [True, True, False]
            elif self.world.fire_1.stat == [True, True, False]:
                self.world.fire_1.stat = [True, True, True]

    def come_back(self):
        self.stat = True
        self.x = 2000
        self.y = randint(300, 500)

    def reset(self):
        self.come_back()


class AnotherHeart:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 10
        self.stat = True

    def update(self, delta):
        if self.stat:
            if self.x <= 0:
                self.come_back()
            else:
                self.x -= self.vx

    def hit(self):
        if self.x - 20 <= self.world.player.x <= self.x + 20 and self.y - 50 <= self.world.player.y <= self.y + 50:
            arcade.sound.play_sound(self.world.heart_sound)
            self.x = 0
            self.y = 0
            self.stat = False
            self.world.life += 1
            self.come_back()

    def come_back(self):
        self.stat = True
        self.x = 5000
        self.y = randint(200, 540)

    def reset(self):
        self.come_back()


class Bonus:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 10
        self.stat = True

    def update(self, delta):
        if self.stat:
            if self.x <= 0:
                self.come_back()
            else:
                self.x -= self.vx

    def hit(self):
        if self.x - 20 <= self.world.player.x <= self.x + 20 and self.y - 40 <= self.world.player.y <= self.y + 40:
            self.x = 0
            self.y = 0
            self.stat = False
            self.world.bonus_stat = True
            self.come_back()

    def come_back(self):
        self.stat = True
        self.x = 4000
        self.y = randint(200, 540)
        self.world.bonus_time = 10

    def reset(self):
        self.come_back()


class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.state = World.STATE_FROZEN
        self.next_direction = DIR_STILL
        self.bonus_stat = False
        self.bonus_time = 10
        self.score_reach = 500
        self.score = 0
        self.level = 1
        self.life = 5
        self.background = Decoration(self, 650, 300)
        self.start_game = Decoration(self, 650, 300)
        self.end = Decoration(self, 650, 300)
        self.help = Decoration(self, 650, 300)
        self.heart_life = Decoration(self, 305, 560)
        self.bonus = Bonus(self, 10000, randint(200, 540))
        self.bonus_1 = Decoration(self, 400, 560)
        self.bonus_2 = Decoration(self, 400, 560)
        self.another_heart = AnotherHeart(self, 2000, randint(200, 540))
        self.player = Player(self, 80, 130)
        self.fire_1 = Fire(self, 150, 130)
        self.fire_2 = Fire(self, 150, 130)
        self.fire_3 = Fire(self, 150, 130)
        self.another_fire = AnotherFire(self, 2000, randint(200, 540))
        self.zombie = Zombie(self, 1500, 120)
        self.grim = Grim(self, 2500, 130)
        self.ghost = Ghost(self, 3500, randint(300, 520))
        self.witch = Witch(self, 4500, randint(300, 520))
        self.TinkerBell = TinkerBell(self, 6500, randint(300, 520))
        self.Ariel = Ariel(self, 7500, 130)
        self.fire_sound = arcade.sound.load_sound("sounds/Attack.wav")
        self.hit_sound = arcade.sound.load_sound("sounds/Burning.wav")
        self.heart_sound = arcade.sound.load_sound("sounds/Heart.wav")
        self.start_sound = arcade.sound.load_sound("sounds/Start.wav")
        self.level_up_sound = arcade.sound.load_sound("sounds/Level_up.wav")
        self.end_sound = arcade.sound.load_sound("sounds/End.wav")

    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return
        if self.state == 2:
            self.level_up()
            self.bonus_up()
            if self.is_end():
                self.end_game()
            self.player.update(delta)
            self.bonus.update(delta)
            self.bonus.hit()
            self.zombie.hit()
            self.grim.hit()
            self.ghost.hit()
            self.witch.hit()
            self.TinkerBell.hit()
            self.Ariel.hit()
            self.another_fire.hit()
            self.another_heart.hit()
            self.fire_1.update(delta)
            self.fire_2.update(delta)
            self.fire_3.update(delta)
            self.zombie.update(delta)
            self.grim.update(delta)
            self.ghost.update(delta)
            self.witch.update(delta)
            self.TinkerBell.update(delta)
            self.Ariel.update(delta)
            self.another_fire.update(delta)
            self.another_heart.update(delta)

    def start(self):
        arcade.sound.play_sound(self.start_sound)
        self.state = World.STATE_STARTED

    def is_started(self):
        return self.state == World.STATE_STARTED

    def is_end(self):
        return self.life <= 0

    def end_game(self):
        arcade.sound.play_sound(self.end_sound)
        self.state = World.STATE_DEAD

    def reset(self):
        self.state = World.STATE_FROZEN
        self.life = 5
        self.score = 0
        self.score_reach = 500
        self.level = 1
        self.player.reset()
        self.zombie.reset()
        self.grim.reset()
        self.ghost.reset()
        self.witch.reset()
        self.TinkerBell.reset()
        self.Ariel.reset()
        self.fire_1.reset()
        self.bonus.reset()
        self.another_heart.reset()

    def fire_on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.fire_1.attack()
            arcade.sound.play_sound(self.fire_sound)
            if self.fire_1.x > 150 and (
                    self.fire_1.stat == [True, True, False] or self.fire_1.stat == [True, True, True]):
                self.fire_2.attack()
                arcade.sound.play_sound(self.fire_sound)
                if self.fire_1.x > 150 and self.fire_2.x >= 200 and self.fire_1.stat == [True, True, True]:
                    self.fire_3.attack()
                    arcade.sound.play_sound(self.fire_sound)

    def player_on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.player.jump()

    def level_up(self):
        if self.score >= self.score_reach:
            arcade.sound.play_sound(self.level_up_sound)
            self.level += 1
            self.score_reach += 500
            self.zombie.vx += 0.5
            self.zombie.vyy += 0.5
            self.grim.vx += 0.5
            self.ghost.vx += 0.5
            self.witch.vx += 0.5
            self.Ariel.vx += 0.5
            self.TinkerBell.vx += 0.5

    def bonus_up(self):
        if self.bonus_stat:
            self.zombie.score = 30
            self.grim.score = 40
            self.ghost.score = 40
            self.witch.score = 40
            self.Ariel.score = -100
            self.TinkerBell.score = -100
            self.bonus_time -= 0.022
            if self.bonus_time <= 0:
                self.bonus_stat = False
        else:
            self.zombie.score = 30
            self.grim.score = 20
            self.ghost.score = 20
            self.witch.score = 20
            self.Ariel.score = -100
            self.TinkerBell.score = -100

    def reset_on_key_press(self, key, key_modifiers):
        if self.state == 3 and key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
            self.reset()
        elif self.state == 3 and key == arcade.key.ESCAPE:
            sys.exit()
