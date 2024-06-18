import pygame

from random import randint, choice


#Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.player_walk = [pygame.image.load(f'assets/player/player{i}.png').convert_alpha() for i in range(1, 9)]
        self.animation_index = 0
        self.player_jump = pygame.image.load('assets/player/player_jump.png')

        self.image = self.player_walk[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (30,184))
        self.gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.rect.bottom >= 186:
            self.gravity = -14
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 186:
            self.rect.bottom = 186

    def animation(self):
        if self.rect.bottom < 186:
            self.image = self.player_jump
        else:
            self.animation_index += 0.2
            if self.animation_index >= len(self.player_walk):
                self.animation_index = 0

            self.image = self.player_walk[int(self.animation_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'bat':
            self.frames = [pygame.image.load(f'assets/bat/bat{i}.png').convert_alpha() for i in range(1, 5)]
            y = 130
        else:
            self.frames = [pygame.image.load(f'assets/slime/slime{i}.png').convert_alpha() for i in range(1, 5)]
            y = 186

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(500,600),y))

    def animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0

        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x < -50:
            self.kill()
    
    def update(self):
        self.animation()
        self.rect.x -= 5
        self.destroy()

#Function
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f'Score: {current_time}',False,(255,255,255))
    score_rect = score_surf.get_rect(center = (384/2,40))
    screen.blit(score_surf,score_rect)
    return current_time 

def collisions():
    if pygame.sprite.spritecollide(player.sprite, enemy_group, False):
        enemy_group.empty()
        return False
    else:
        return True


# pygame setup
pygame.init()
screen = pygame.display.set_mode((384, 216))
clock = pygame.time.Clock()


active = True
start_time = 0
score = 0
font = pygame.font.Font('assets/PixelifySans.ttf',30)

background = pygame.image.load('assets/background.png')
ground = pygame.image.load('assets/ground.png')

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

enemy_group = pygame.sprite.Group()

#Timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)

while True:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if active:
            if event.type == enemy_timer:
                enemy_group.add(Enemy(choice(['bat','slime','slime'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                active = True
                start_time = int(pygame.time.get_ticks() / 1000)
    

    # RENDER YOUR GAME HERE

    if active:
        screen.blit(background, (0,0))
        screen.blit(ground, (0,184))
        score = display_score()

        player.draw(screen)
        player.update()

        enemy_group.draw(screen)
        enemy_group.update()

        active = collisions()

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
