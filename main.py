import pygame, sys
from pygame.locals import QUIT
from sprites import *
from config import *


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.screen.fill(BLACK)
        self.caption = pygame.display.set_caption('First Game')
        self.clock = pygame.time.Clock()
        self.running = True
        self.key = False
        self.health = HEALTH
        self.level = 0

        self.font = pygame.font.Font("CormorantGaramond-Bold.ttf", 50)

        print("Current lives: 1")

    def createMap(self, level):
        self.walls = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()

        for i, row in enumerate(level):
            for j, column in enumerate(row):
                if column == 'W':
                    w = Wall(self, j, i)
                    self.walls.add(w)

                if column == 'P':
                    p = Player(self, j, i, 3)
                    self.players.add(p)
                if column == 'H':
                    h = Heart(self, j, i)
                    self.hearts.add(h)
                if column == 'K':
                    k = Key(self, j, i)
                    self.keys.add(k)

                if column == 'M':
                    m = Monster(self, j, i)
                    self.monsters.add(m)

                if column == 'L':
                    if row[j + 1] == 'M':
                        direction = "left"
                    if row[j - 1] == 'M':
                        direction = 'right'
                    if level[i + 1][j] == 'M':
                        direction = 'down'
                    if level[i - 1][j] == 'M':
                        direction = 'up'
                    l = Laser(self, j, i, 1, direction, "zError.png", False)
                    self.lasers.add(l)

                if column == 'B':
                    b = Boss(self, j, i, 1)
                    self.boss.add(b)
                    lb1 = Laser(self, j, i, 1, "left", "zKeyErr.png", True)
                    self.lasers.add(lb1)
                    lb2 = Laser(self, 12, 4, 2, "down", "zNameErr.png", True)
                    self.lasers.add(lb2)

    def new(self, level):
        # a new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.wall = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.collectables = pygame.sprite.LayeredUpdates()

        self.createMap(level)

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        # game loop updates
        self.all_sprites.update()

    def draw(self):
        # game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()  # press keys
            self.update()  # make changes
            self.draw()  # display

    def display_text(self):
        t_heart = Text(self, 780, 20, "Heart: ")
        t_key = Text(self, 20, 20, "Key: ")

        t_heart.displaying(self.health)
        t_key.displaying(self.key)

    def game_over(self):
        print("Game Over. Failed to de\"bug\". You lose.")
        pygame.quit()
        sys.exit()

    def intro_screen(self):
        intro = True
        title = self.font.render("Hack Crushers", True, WHITE)
        title_rect = title.get_rect(x=20, y=20)

        start_button = Button(g, 100, 150, "zStart.png")
        exit_button = Button(g, 300, 150, "zExit.png")

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            if start_button.draw():
                intro = False

            if exit_button.draw():
                intro = False
                self.running = False

            self.screen.blit(title, title_rect)

            self.clock.tick(FPS)
            pygame.display.update()

    def next_level(self):
        if self.level < 3:
            self.level += 1
        self.key = False


g = Game()

g.intro_screen()

while g.running:
    g.new(levelnum[g.level])
    g.main()

    if g.health <= 0:
        g.game_over()

    for wall in g.walls:
        wall.kill()
        g.screen.fill(BLACK)
        continue

pygame.quit()
sys.exit()
