from pygame import key
from pygame.time import Clock
import pygame
from pygame.constants import USEREVENT
from random import randint
from player import player
from menu import menu

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
lives = 1
score = 0
gameover = False
pygame.display.set_caption("Mygame")
pygame.display.set_icon(icon)
pygame.mixer.music.play(-1)
pygame.time.set_timer(ENEMIES, enemie_time)
fade.fill((255, 255, 255))


class projectile (object):
    def __init__(self, x, y, vel, angle):
        self.bullet = pygame.image.load('projectile/bullet.png')
        self.x = x
        self.y = y
        self.angle = angle
        self.vel = vel

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
    elif man.action == 'death':
        man.isflip = False
        man.draw(win, man.death, 10)
        man.health = 100

    win.blit(background[1], (0, 0))
    if gameover:
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


man = player(0, 310, 96, 98, 7, 'player_1',2)
enemies = []
bullets = []
while run:
    clock.tick(27)
    if man.health <= 0 and lives > 0 and man.action != 'death':
        man.action = 'death'
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
    if lives>0:
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
                if man.action in [ 'walk_right','idle','walk_up'] and len(bullets) < 10 and man.bullet_delay > 400:
                    man.bullet_delay = 0
                    bullets.append(projectile(round(man.x + man.width//2),
                                            round(man.y+man.height//2), 2, 0))
                elif man.action == 'walk_left' and len(bullets) < 10 and man.bullet_delay > 400:
                    man.bullet_delay = 0
                    bullets.append(projectile(round(man.x + man.width//2-10),
                                            round(man.y+man.height//2), -2, 180))
        if man.action != 'death':
            if keys[pygame.K_LEFT] and man.x > man.vel-60:
                man.x -= man.vel
                man.action = 'walk_left'
            elif keys[pygame.K_RIGHT] and man.x < 764-man.width-man.vel:
                man.x += man.vel
                man.x += man.vel
                man.action = 'walk_right'
            elif keys[pygame.K_UP] and man.y > 130:
                man.y -= man.vel
                man.action = 'walk_up'
            elif keys[pygame.K_DOWN] and man.y < 360-man.vel:
                man.y += man.vel
                man.action = 'idle'
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
                if enemy.health <= 0:
                    score += 2000*enemy.power
                    enemy.action = 'death'
                    health_gain = pygame.mixer.Sound('audio/health_recharge.wav')
                    health_gain.play()
                    enemies.pop(enemies.index(enemy))
                    if man.health <= 80:
                        man.health += 20
                    else:
                        man.health = 100
                elif enemy.x <= -60:
                    enemies.pop(enemies.index(enemy))
                    lives -= 1
                elif man.action in ['attack', 'l_attack'] and int(man.x) in range(enemy.x - 65, enemy.x + 65) and int(man .y) in range(enemy.y - 40, enemy.y + 40):
                    enemy.action = 'hurt'
                    # enemy.x += 4
                    enemy.health -= man.power
                    score += 3
                elif enemy.x in range(int(man.x) - 60, int(man.x)) and enemy .y in range(int(man.y) - 35, int(man.y) + 35) and enemy.can_attack and man.action != 'death':
                    enemy.action = 'attack'
                    man.health -= enemy.power
                    man.action = 'hurt'
                    # man.x += 4
                elif enemy.x in range(int(man.x), int(man.x) + 60) and enemy .y in range(int(man.y) - 35, int(man.y) + 35) and enemy.can_attack and man.action != 'death':
                    enemy.action = 'l_attack'
                    man.health -= enemy.power
                    man.action = 'hurt'
                    # man.x -= 4
                if enemy.action not in ['attack','l_attack','hurt']:
                    enemy.x -= enemy.vel

            for bullet in bullets:
                for enemy in enemies:
                    if int(bullet.x) in range(enemy.x+25, enemy.x+75) and int(bullet .y) in range(enemy.y + 23, enemy.y+68):
                        bullets.pop(bullets.index(bullet))
                        enemy.action = 'hurt'
                        enemy.health -= 8
                        score += 5
                        bullet_hit = True
                        break
                if bullet_hit:
                    bullet_hit = False
                    continue
                if bullet.x < 700 and bullet.x > 0 :
                    bullet.x += bullet.vel
                else:
                    bullets.pop(bullets.index(bullet))
                    
    refreshGameWindow()
