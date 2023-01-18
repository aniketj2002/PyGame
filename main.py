from pygame import key
from pygame.time import Clock
import pygame
from pygame.constants import USEREVENT
from random import randint
pygame .init()


background = [pygame.image.load(
    'background/img1.png'), pygame.image.load('background/img2.png')]
icon = pygame.image.load("icon/icon.png")
font = pygame.font.Font('freesansbold.ttf', 26)
music = pygame.mixer.music.load('audio/bg_music.mp3')
win = pygame.display.set_mode((700, 500))
fade = pygame.Surface((700, 500))
clock = pygame.time.Clock()
over = pygame.image.load("game_over/game_over.png")
ENEMIES = USEREVENT + 1
enemie_time = 10000
bullet_hit = False
run = True
lives = 3
score = 0
gameover = False
pygame.display.set_caption("Knight")
pygame.display.set_icon(icon)
pygame.mixer.music.play(-1)
pygame.time.set_timer(ENEMIES, enemie_time)
fade.fill((255, 255, 255))


class player(object):
    def __init__(self, x, y, width, height, vel, folder_name):
        self.walk = [pygame.image.load(folder_name + "/run1.png"), pygame.image.load(folder_name + "/run2.png"), pygame.image.load(folder_name + "/run3.png"), pygame.image.load(folder_name + "/run4.png"),
                     pygame.image.load(folder_name + "/run5.png"), pygame.image.load(folder_name + "/run6.png"), pygame.image.load(folder_name + "/run7.png"), pygame.image.load(folder_name + "/run8.png")]
        self.climb = [pygame.image.load(folder_name + "/climb1.png"), pygame.image.load(folder_name + "/climb2.png"),
                      pygame.image.load(folder_name + "/climb3.png"), pygame.image.load(folder_name + "/climb4.png")]
        self.idle = [pygame.image.load(folder_name + "/idle1.png"), pygame.image.load(folder_name + "/idle2.png"), pygame.image.load(folder_name + "/idle3.png"), pygame.image.load(folder_name + "/idle4.png"), pygame.image.load(folder_name + "/idle5.png"), pygame.image.load(folder_name + "/idle6.png"), pygame.image.load(
            folder_name + "/idle7.png"), pygame.image.load(folder_name + "/idle7.png"), pygame.image.load(folder_name + "/idle8.png"), pygame.image.load(folder_name + "/idle9.png"), pygame.image.load(folder_name + "/idle10.png"), pygame.image.load(folder_name + "/idle11.png"), pygame.image.load(folder_name + "/idle12.png")]
        self.attack = [pygame.image.load(folder_name + "/run_attack1.png"), pygame.image.load(folder_name + "/run_attack2.png"), pygame.image.load(folder_name + "/run_attack3.png"), pygame.image.load(folder_name + "/run_attack4.png"), pygame.image.load(folder_name + "/run_attack5.png"), pygame.image.load(folder_name + "/run_attack6.png"), pygame.image.load(
            folder_name + "/run_attack7.png"), pygame.image.load(folder_name + "/run_attack8.png")]
        self.hurt = [pygame.image.load(folder_name + "/hurt1.png"), pygame.image.load(folder_name + "/hurt2.png"),
                     pygame.image.load(folder_name + "/hurt3.png"), pygame.image.load(folder_name + "/hurt4.png")]
        self.death = [pygame.image.load(folder_name + "/death1.png"), pygame.image.load(folder_name + "/death2.png"), pygame.image.load(folder_name + "/death3.png"), pygame.image.load(folder_name + "/death4.png"), pygame.image.load(folder_name + "/death5.png"), pygame.image.load(folder_name + "/death6.png"), pygame.image.load(
            folder_name + "/death7.png"), pygame.image.load(folder_name + "/death8.png"), pygame.image.load(folder_name + "/death9.png"), pygame.image.load(folder_name + "/death10.png")]

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.jumpcount = 6
        self.health = 100
        self.count = 0
        self.isjumping = False
        self.can_attack = True
        self.action = 'idle'
        self.isflip = False
        self.is_attacked = False
        self.pre_frame = 'idle'
        self.pre_action = 'idle'
        self.attack_delay = 0
        self.count_2 = 0
        self.time_attack_delay = pygame.time.Clock()
        self.bullet_delay = 0
        self.time_bullet_delay = pygame.time.Clock()

    def draw(self, win, image_set, num_of_images):
        if self.count + 1 >= num_of_images*3:
            self.count = 0
        if self.count_2 + 1 >= num_of_images*3:
            self.count_2 = 0
            if self.action == 'death':

                self.action = 'idle'
                self.x = 0
                self.y = 310
            self.action = self.pre_action
        if self.action != self.pre_frame and self.action not in ['idle', 'walk_up', 'walk_right', 'walk_left', 'hurt']:
            self.sound = pygame.mixer.Sound('audio/' + self.action + '.wav')
            self.sound.play()

        self.health_com = abs(int(self.health)/100*60)
        pygame.draw.rect(win, (255-self.health_com*4, self.health_com*4,
                               0), (self.x+20, self.y, self.health_com, 8))
        pygame.draw.rect(win, (0, 0, 0), (self.x+20, self.y, 60, 10), 2)

        if self.action in ['hurt', 'attack', 'l_attack', 'death']:
            win.blit(pygame.transform.flip(
                image_set[self.count_2//3], self.isflip, False), (self.x, self.y))
            self.count_2 += 1

        else:
            win.blit(pygame.transform.flip(
                image_set[self.count//3], self.isflip, False), (self.x, self.y))
            self.count += 1
            self.pre_action = self.action
        self.pre_frame = self.action
        if self.action in ['walk_up', 'walk_right', 'walk_left'] and self.count != 9 and self.count != 20 and self.count % 3 == 0:
            self.sound = pygame.mixer.Sound('audio/' + self.action + '.wav')
            self.sound.play()


class projectile (object):
    def __init__(self, x, y, vel, angle):
        self.bullet = pygame.image.load('projectile/bullet.png')
        self.x = x
        self.y = y
        self.angle = angle
        self.vel = vel
        self.dir = 'vertical'
        if ((self.angle)/90) % 2 == 0:
            self.dir = 'horizontal'

    def draw_bullet(self, win):
        win.blit(pygame.transform.rotate(
            self.bullet, self.angle), (self.x, self.y))


def refreshGameWindow():
    win.blit(background[0], (0, 0))

    for enemy in enemies:
        enemy.isflip = True
        if enemy.action == 'hurt':
            enemy.isflip = False
            enemy.draw(win, enemy.hurt, 4)
        elif enemy.action == 'attack':
            enemy.isflip = False
            enemy.draw(win, enemy.attack, 8)
        elif enemy.action == 'l_attack':
            enemy.isflip = True
            enemy.draw(win, enemy.attack, 8)
        elif enemy.action == 'death':
            enemy.isflip = True
            enemy.draw(win, enemy.attack, 10)
        else:
            enemy.draw(win, enemy.walk, 8)

    for bullet in bullets:
        bullet.draw_bullet(win)

    if man.action == 'idle':
        man.isflip = False
        man.draw(win, man.idle, 12)
    elif man.action == 'walk_right':
        man.isflip = False
        man.draw(win, man.walk, 8)
    elif man.action == 'walk_left':
        man.isflip = True
        man.draw(win, man.walk, 8)
    elif man.action == 'walk_up':
        man.isflip = False
        man.draw(win, man.climb, 4)
    elif man.action == 'attack':
        man.isflip = False
        man.draw(win, man.attack, 8)
    elif man.action == 'l_attack':
        man.isflip = True
        man.draw(win, man.attack, 8)
    elif man.action == 'hurt':
        man.isflip = False
        man.draw(win, man.hurt, 4)
    # elif man.action == 'death':
    #     man.isflip = False
    #     man.draw(win, man.death, 10)
    #     man.health = 100

    win.blit(background[1], (0, 0))
    if gameover or man.action =='death':
        pass
    else:
        text = font.render('Score ', True, (255, 255, 255))
        win.blit(text, (588, 439))
        text = font.render(str(score//10), True, (255, 255, 255))
        win.blit(text, (610, 465))
        text = font.render('Lives ', True, (255, 255, 255))
        win.blit(text, (70, 30))
        text = font.render(str(lives), True, (255, 255, 255))
        win.blit(text, (92, 56))
        pygame.display.update()


man = player(0, 310, 96, 98, 7, 'player_1')
enemies = []
bullets = []
while run:
    clock.tick(27)
    if man.health <= 0 and lives > 0 and man.action != 'death':
        man.action = 'death'
        for a in range (30):
            refreshGameWindow()
            man.draw(win,man.death,10)
            pygame.display.update()
        man.health = 100

        lives -= 1
    elif lives <= 0:
        over_music = pygame.mixer.Sound('audio/game_over.wav')
        over_music.play()
        Gameover = True
        for alpha in range(0, 300):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            fade.set_alpha(alpha)
            win.blit(fade, (0, 0))
            text = font.render(
                'Score '+str(int(score/10)), True, (0, 0, 0))
            win.blit(text, (558, 439))
            win.blit(over, (150, 150))
            pygame.display.update()
            pygame.time.delay(15)
        alpha = 300
        win.blit(fade, (0, 0))
        text = font.render(
            'Esc to Quit or Enter to Restart Game '+str(int(score/10)), True, (0, 0, 0))
        win.blit(text, (150, 240))
        pygame.display.update()
        exit()
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            run = False
        elif event.type == ENEMIES:
            enemies.append(player(700, randint(50, 170) +
                           randint(50, 170), 96, 98, 1, 'enemy_1'))

        if man.action == 'hurt':
            man.can_attack = False
        else:
            man.can_attack = True
        man.bullet_delay += (man.time_bullet_delay).tick()
        if keys[pygame.K_a] and man.can_attack:
            if man.action == 'walk_right':
                man.action = 'attack'
            elif man.action == 'walk_left':
                man.action = 'l_attack'
        if keys[pygame.K_d] and man.can_attack:
            if man.action == 'walk_up' and len(bullets) < 10 and man.bullet_delay > 400:
                man.bullet_delay = 0
                bullets.append(projectile(round(man.x + man.width//4),
                                          round(man.y+man.height//2), -2, 90))
            elif man.action == 'idle' and len(bullets) < 10 and man.bullet_delay > 400:
                man.bullet_delay = 0
                bullets.append(projectile(round(man.x + man.width//4),
                                          round(man.y+man.height//2+40), 2, 270))
            elif man.action == 'walk_right' and len(bullets) < 10 and man.bullet_delay > 400:
                man.bullet_delay = 0
                bullets.append(projectile(round(man.x + man.width//4),
                                          round(man.y+man.height//2+20), 2, 0))
            elif man.action == 'walk_left' and len(bullets) < 10 and man.bullet_delay > 400:
                man.bullet_delay = 0
                bullets.append(projectile(round(man.x + man.width//4),
                                          round(man.y+man.height//2+20), -2, 180))
    if man.action != 'death':
        if keys[pygame.K_LEFT] and man.x > man.vel-60:
            man.x -= man.vel
            man.action = 'walk_left'
        elif keys[pygame.K_RIGHT] and man.x < 764-man.width-man.vel:
            man.x += man.vel
            man.action = 'walk_right'
        elif keys[pygame.K_UP] and man.y > 100:
            man.y -= man.vel
            man.action = 'walk_up'
        elif keys[pygame.K_DOWN] and man.y < 340-man.vel:
            man.y += man.vel
            man.action = 'idle'
            pygame.mixer.Sound('audio/walk_down.wav').play()
        elif man.action == 'walk_up':
            man.count = 8
        elif man.action == 'walk_right' or man.action == 'walk_left':
            man.count = 19
        if not (man.isjumping):
            if keys[pygame.K_SPACE]:
                man.isjumping = True
                jump_sound = pygame.mixer.Sound('audio/jump.wav')
                jump_sound.play()
        else:
            if man.jumpcount >= -6:
                neg = 0.5
                if man.jumpcount < 0:
                    neg = -1*0.5
                man.y -= (man.jumpcount**2)*neg
                man.jumpcount -= 1
            else:
                man.isjumping = False
                man.jumpcount = 6
        for enemy in enemies:
            if enemy.action == 'hurt':
                enemy.can_attack = False
            else:
                enemy.can_attack = True
            enemy.x -= enemy.vel
            if enemy.health <= 0:
                score += 400
                enemy.action = 'death'
                health_gain = pygame.mixer.Sound('audio/health_recharge.wav')
                health_gain.play()
                enemies.pop(enemies.index(enemy))
                if man.health <= 80:
                    man.health += 20
                else:
                    man.health = 100
            elif enemy.x <= -100:
                enemies.pop(enemies.index(enemy))

                lives -= 1
            elif man.action in ['attack', 'l_attack'] and int(man.x) in range(enemy.x - 30, enemy.x + 90) and int(man .y) in range(enemy.y - 30, enemy.y + 30):
                enemy.action = 'hurt'
                enemy.health -= 1.5
                score += 2

            elif man.action in ['attack', 'l_attack'] and enemy.x in range(int(man.x) - 30, int(man.x) + 30) and enemy .y in range(int(man.y) - 30, int(man.y) + 30):
                enemy.action = 'hurt'
                enemy.health -= 1.5
                score += 2

            elif int(man.x) in range(enemy.x - 30, enemy.x + 30) and int(man .y) in range(enemy.y - 30, enemy.y + 30) and enemy.can_attack and man.action != 'death':
                enemy.action = 'l_attack'
                man.health -= 2
                man.action = 'hurt'
                man.x -= 4

            elif enemy.x in range(int(man.x) - 30, int(man.x) + 30) and enemy .y in range(int(man.y) - 30, int(man.y) + 30) and enemy.can_attack and man.action != 'death':
                enemy.action = 'attack'
                man.health -= 0.2
                man.action = 'hurt'
                man.x += 4

        for bullet in bullets:
            for enemy in enemies:
                if int(bullet.x) in range(enemy.x+60, enemy.x+75) and int(bullet .y) in range(enemy.y + 50, enemy.y+95):
                    bullets.pop(bullets.index(bullet))
                    enemy.action = 'hurt'
                    enemy.health -= 8
                    score += 5
                    bullet_hit = True
                    break
            if bullet_hit:
                bullet_hit = False
                continue
            if bullet.y < 410 and bullet.y > 160 and bullet.dir == 'vertical':
                bullet.y += bullet.vel
            elif bullet.x < 700 and bullet.x > 0 and bullet.dir == 'horizontal':
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
    refreshGameWindow()
