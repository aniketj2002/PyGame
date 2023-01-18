import pygame
class player(object):
    def __init__(self, x, y, width, height, vel, folder_name,power=0.2):
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
        self.power=power

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
        if self.action != 'death':
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
