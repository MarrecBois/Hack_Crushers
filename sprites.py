from config import *
import pygame
import time


class Stat(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def moveIt(self):
        self.rect.x = 15 * SCALER
        self.rect.y = 20 * SCALER


class Monster(Stat):
    counter = 0

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        image = pygame.image.load("zBug.png")
        self.image = pygame.Surface([self.width + 120, self.height + 60])
        self.image.set_colorkey(WHITE)
        self.image.blit(image, (x, y - 10))

        self._layer = COLLECT_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect.update(self.rect.x, self.rect.y, 3 * SCALER, 2 * SCALER)


class Boss(Monster):

    def __init__(self, game, x, y, form):
        self.form = form

        super().__init__(game, x, y)

        self.image = pygame.Surface([self.width + 160, self.height + 140])
        self.change_form()
        image = pygame.image.load(self.image_name)
        self.image.blit(image, (x, y))

        self.rect.update(self.rect.x, self.rect.y, 4 * SCALER, 5 * SCALER)

    def change_form(self):
        if self.form == 1:
            self.image_name = "zBoss1.png"
        if self.form == 2:
            self.image_name = "zBoss2.png"
        if self.form == 3:
            self.image_name = "zBoss3.png"


#Wall Class
class Wall(Stat):

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.image.fill(BLUE)
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.wall
        pygame.sprite.Sprite.__init__(self, self.groups)


class Heart(Stat):

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        image = pygame.image.load("zHeart.png")
        self.image = pygame.Surface([self.width + 20, self.height + 10])
        self.image.set_colorkey(WHITE)
        self.image.blit(image, (x, y))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self._layer = COLLECT_LAYER
        self.groups = self.game.all_sprites, self.game.collectables
        pygame.sprite.Sprite.__init__(self, self.groups)


class Key(Stat):

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        image = pygame.image.load("zKey.png")
        self.image = pygame.Surface([self.width + 95, self.height + 10])
        self.image.set_colorkey(WHITE)
        self.image.blit(image, (x, y))

        self._layer = COLLECT_LAYER
        self.groups = self.game.all_sprites, self.game.collectables
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect.update(self.rect.x, self.rect.y, 4 * SCALER, 1 * SCALER)


class Obj(Stat):

    def __init__(self, game, x, y, velocity):
        super().__init__(game, x, y)
        self.velocity = velocity

        self.x_change = 0
        self.y_change = 0

    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        pass


class Button:

    def __init__(self, game, x, y, image):
        self.game = game
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = pygame.Surface([self.width * 4, self.height * 2])
        self._layer = PLAYER_LAYER
        self.im = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        #draw the button on screen
        self.game.screen.blit(self.im, (self.rect.x, self.rect.y))

        #get mouse position
        pos = pygame.mouse.get_pos()

        #Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action


class Laser(Obj):

    def __init__(self, game, x, y, velocity, direction, image_name, b_c):
        super().__init__(game, x, y, velocity)
        self.direction = direction
        self.load_image = pygame.image.load(image_name)

        self._layer = LASER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.b_c = b_c
        # True -> Bounce

        self.rect.update(self.rect.x, self.rect.y, 3 * SCALER, 1 * SCALER)

    def update(self):
        self.moving(self.direction)

    def moving(self, direction):
        for laser in self.game.lasers:
            self.game.screen.blit(laser.load_image,
                                  (laser.rect.x, laser.rect.y))

        if direction == 'right' or direction == 'left':
            d = 'x'
        elif direction == 'up' or direction == 'down':
            d = 'y'
        if self.collide_blocks(d):
            if self.b_c:
                self.bounce()
            else:
                self.moveIt()

        if direction == "right":
            self.rect.x += self.velocity
        elif direction == "left":
            self.rect.x -= self.velocity
        elif direction == "up":
            self.rect.y += self.velocity
        elif direction == "down":
            self.rect.y -= self.velocity

            pygame.display.update()
            self.game.clock.tick(FPS)

    def moveIt(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def bounce(self):
        self.velocity = -self.velocity

    def collide_blocks(self, direction):
        if direction == 'x':
            return pygame.sprite.spritecollide(self, self.game.walls, False)

        if direction == 'y':
            return pygame.sprite.spritecollide(self, self.game.walls, False)


class Player(Obj):

    def __init__(self, game, x, y, velocity):
        super().__init__(game, x, y, velocity)

        image = pygame.image.load("zGeek.png")
        self.image = pygame.Surface([self.width, self.height + 20])
        self.image.set_colorkey(WHITE)
        self.image.blit(image, (x, y))
        self.count = 1

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            #for sprite in self.game.all_sprites:
            #  sprite.rect.x += self.velocity
            self.x_change -= self.velocity
        if keys[pygame.K_d]:
            #for sprite in self.game.all_sprites:
            #  sprite.rect.x -= self.velocity
            self.x_change += self.velocity
        if keys[pygame.K_w]:
            #for sprite in self.game.all_sprites:
            #  sprite.rect.y += self.velocity
            self.y_change -= self.velocity
        if keys[pygame.K_s]:
            #for sprite in self.game.all_sprites:
            #  sprite.rect.x -= self.velocity
            self.y_change += self.velocity

    #Collision detection
    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_monster(self):
        for monster in self.game.monsters:
            if (self.rect).colliderect(monster.rect) and self.count == 1:
                self.count += 1
                print(self.count)
                print("Quick! You must remove this bug from my computer!")
                time.sleep(1.5)
                print("Why does this code lead to an error?")
                time.sleep(1)
                print("This is the current code:")
                print("print(Hello programmer, I am your first bug to fix)")
                time.sleep(2.5)
                print(
                    "Please choose the option that will lead to no error from the options below:"
                )
                time.sleep(1)
                print(
                    "a. print 'Hello programmer, I am your first bug to fix'")
                print(
                    "b. print('Hello programmer, I am your first bug to fix')")
                print(
                    "c. output(Hello programmer, I am your first bug to fix)")
                print(
                    "d. print(str(Hello programmer, I am your first bug to fix))"
                )
                answer = input("The correct answer is: ")

                if answer in ['b', 'B']:
                    print("CORRECT!")
                    monster.moveIt()

                else:
                    print("Incorrect! The bug is now hurting you too!")

                time.sleep(2)

            elif (self.rect).colliderect(monster.rect) and self.count == 2:
                print("Quick! You must remove this bug from my computer!")
                time.sleep(1.5)
                print("Why does this code lead to an error?")
                time.sleep(1)
                print("This is the current code:")
                print("a = 3 x 5")
                print(
                    "print('Since 3 x 5 = 15, a =', a)	#We want to have a = 15"
                )
                time.sleep(2.5)
                print(
                    "Please choose the option that will lead to no error and output the desired result"
                )
                time.sleep(1)
                print("a. a = 3 x 5")
                print("print('Since 3 x 5 = 15, a = a')")
                print("b. a = 3 x 5")
                print("print('Since 3 x 5 = 15, a = int(a)')")
                print("c. a = 3 * 5")
                print("print('Since 3 x 5 = 15, a =', a)")
                print("d. a = 3 * 5")
                print("print('Since 3 x 5 = 15, a = a')")
                answer = input("The correct answer is: ")

                if answer in ['c', 'C']:
                    print("CORRECT!")
                    monster.moveIt()

                else:
                    print("Incorrect! The bug is now hurting you too!")

            break

    def collide_heart(self):
        for heart in self.game.hearts:
            if (self.rect).colliderect(heart.rect):
                heart.moveIt()
                self.game.health += 1
                print("Current lives: " + str(self.game.health))

    def collide_key(self):
        for key in self.game.keys:
            if (self.rect).colliderect(key.rect):
                key.moveIt()
                self.game.key = True

    def collide_laser(self):
        for laser in self.game.lasers:
            if (self.rect).colliderect(laser.rect):
                laser.moveIt()

                if self.game.health >= 2:
                    self.game.health -= 1
                    print("Current lives: " + str(self.game.health))
                else:
                    self.game.game_over()

                self.rect.x = self.x
                self.rect.y = self.y

    def collide_exit(self):
        if (self.rect).colliderect(
                pygame.Rect(19 * SCALER, 6 * SCALER, 40, 120)):
            if self.game.key:
                self.game.next_level()
                self.game.playing = False
            else:
                self.rect.x = 18 * SCALER

    def collide_boss(self):
        for boss in self.game.boss:
            if (self.rect).colliderect(boss.rect):
                if boss.form == 1:
                    print("I am a super bug!! You will never debug me!!")
                    time.sleep(1.5)
                    print("I want this program to output the number 1738.")
                    time.sleep(1)
                    print(
                        "Please select the code that will output the correct value with no errors."
                    )
                    time.sleep(2.5)
                    print("a. x = 1738")
                    print("print('x')")
                    print("b. x = 0")
                    print("x += 1000")
                    print("x += 700")
                    print("x += 30")
                    print("x += 8")
                    print("print(x)")
                    print("c. x = 1730")
                    print("y = 7")
                    print("print(x + y)")
                    print("d. x = 1730")
                    print("y = 8")
                    print("print('x + y')")
                    answer = input("The correct answer is: ")

                    if answer in ['b', 'B']:
                        print("CORRECT! But you just got lucky...")
                        boss.moveIt()

                    else:
                        print("Incorrect! I will take ALL of your hearts!")
                        if self.game.health >= 2:
                            self.game.health -= 1
                            print("Current lives: " + str(self.game.health))
                        else:
                            self.game.game_over()

                    time.sleep(2)

                    boss.form += 1

                    b2 = Boss(self.game, boss.x, boss.y, boss.form)
                    self.game.boss.add(b2)
                    lb1 = Laser(self.game, 10, 10, 1, "right", "zLogicErr.png",
                                False)
                    self.game.lasers.add(lb1)
                    lb2 = Laser(self.game, 1, 13, 1, "up", "zDivErr.png", True)
                    self.game.lasers.add(lb2)

                elif boss.form == 2:
                    print("I'm not done yet!!! More debugging to go!!")
                    time.sleep(1.5)
                    print("I want this program to output the number 5.")
                    time.sleep(1)
                    print("Function for ALL OPTIONS:")
                    print("def num_add(num):")
                    print("\t return num + 3")
                    time.sleep(1.5)
                    print(
                        "Please select the code that will output the correct value with no errors."
                    )
                    time.sleep(2.5)
                    print("a. x = num_add(5)")
                    print("print(x)")
                    print("b. x = 5")
                    print("x = num_add(1)")
                    print("print(x)")
                    print("c. x = num_add(2)")
                    print("x = 4")
                    print("print(x)")
                    print("d. x = -1")
                    print("y = num_add(num_add(x))")
                    print("print(y)")
                    answer = input("The correct answer is: ")

                    if answer in ['d', 'D']:
                        print("CORRECT! Another lucky guess...")
                        boss.moveIt()

                    else:
                        print("Incorrect! I will take ALL of your hearts!")
                        if self.game.health >= 2:
                            self.game.health -= 1
                            print("Current lives: " + str(self.game.health))
                        else:
                            self.game.game_over()

                    time.sleep(2)

                    boss.form += 1

                    b3 = Boss(self.game, boss.x, boss.y, boss.form)
                    lb1 = Laser(self.game, 1, 8, 1, "right", "zIndexErr.png",
                                True)
                    self.game.lasers.add(lb1)
                    lb2 = Laser(self.game, boss.x, boss.y, 3, "down",
                                "zValueErr.png", False)
                    self.game.lasers.add(lb2)

                elif boss.form == 3:
                    print("One... more... BUG!!!")
                    time.sleep(2)
                    print("What type of error will this code lead to?")
                    time.sleep(1.5)
                    print("This is the current code:")
                    print("def cents_to_dollar(num):")
                    print("\tdollar = num / 100")
                    print("conerted_cash = cents_to_dollar(123)")
                    print("print(dollar)")
                    time.sleep(2.5)
                    print(
                        "Please choose the option that corresponds to the error that will be displayed"
                    )
                    time.sleep(1)
                    print("a. NameError")
                    print("b. SyntaxError")
                    print("c. ValueError")
                    print("d. TypeError")
                    answer = input("The correct answer is: ")

                    if answer in ['a', 'A']:
                        print("CORRECT! NOOO I have been debugged!")
                        boss.moveIt()

                    else:
                        print("Incorrect! I will take ALL of your hearts!")
                        if self.game.health >= 2:
                            self.game.health -= 1
                            print("Current lives: " + str(self.game.health))
                        else:
                            self.game.game_over()

                    time.sleep(2)

                    print("You Win!")

                self.rect.x = self.x
                self.rect.y = self.y

    def update(self):
        super().update()
        self.collide_monster()
        self.collide_heart()
        self.collide_key()
        self.collide_laser()
        self.collide_exit()
        self.collide_boss()
