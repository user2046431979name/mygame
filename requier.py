import pygame
import random
import math

pygame.init()

walk_left = [
    pygame.image.load('images/walk_left/player_left-removebg-preview.png'),
    pygame.image.load('images/walk_left/player_left1-removebg-preview.png'),
    pygame.image.load('images/walk_left/player_left2-removebg-preview.png'),
    pygame.image.load('images/walk_left/player_left3-removebg-preview.png'),
]

walk_right = [
    pygame.image.load('images/walk_right/player_right-removebg-preview.png'),
    pygame.image.load('images/walk_right/player_right1-removebg-preview.png'),
    pygame.image.load('images/walk_right/player_right2-removebg-preview.png'),
    pygame.image.load('images/walk_right/player_right3-removebg-preview.png'),
]

z_right = [
    pygame.image.load("images/zombie/zombie_right1.png"),
    pygame.image.load("images/zombie/zombie_right2.png"),
    pygame.image.load("images/zombie/zombie_right3.png"),
    pygame.image.load("images/zombie/zombie_rigth_attack1.png"),
    pygame.image.load("images/zombie/zombie_right_attack2.png"),
    pygame.image.load("images/zombie/zombie_right_attack3.png"),

]


z_left = [
    pygame.image.load("images/zombie/zombie_left1.png"),
    pygame.image.load("images/zombie/zombie_left2.png"),
    pygame.image.load("images/zombie/zombie_left3.png"),
    pygame.image.load("images/zombie/zombie_left_attack1.png"),
    pygame.image.load("images/zombie/zombie_left_attack2.png"),
    pygame.image.load("images/zombie/zombie_left_attack3.png"),
]

slash_katana = [
    [
    pygame.image.load("images/guns/slash1.png"),
    pygame.image.load("images/guns/slash2.png"),
    pygame.image.load("images/guns/slash3.png"),
    ],
    [
    pygame.image.load("images/guns/katana_ultimate_slash.png"),
    pygame.image.load("images/guns/katana_ultimate_slash.png"),
    ]
]

katana_img = pygame.image.load("images/guns/katana.png")

katana_hit_sounds = pygame.mixer.Sound("sounds/Hit_katana.mp3")
katana_no_hit_sounds = pygame.mixer.Sound("sounds/notHit_katana.mp3")




bullet_img = pygame.image.load('images/bullet_remove-preview.png')




info_user_font = pygame.font.Font('fonts/PixelifySans-VariableFont_wght.ttf',20)
info_damage_font = pygame.font.Font('fonts/PixelifySans-VariableFont_wght.ttf',10)

system_font = pygame.font.Font('fonts/PixelifySans-VariableFont_wght.ttf',35)


























def katanAttack(self,screen,player):

    if player.direct_move == walk_right:
        self.angle = 60
        try:
            player.isAttack = False
            screen.blit(pygame.transform.flip(self.attack_anim[self.attack_count], True, False),
                        (player.pos_x + 30, player.pos_y))
            self.attack_count += 1
            rect = self.attack_anim[self.attack_count].get_rect()
            rect.x = player.pos_x + 30
            rect.y = player.pos_y
            return rect
        except:
            self.attack_count = 0
            self.angle = 0
            player.isAttack = True
            return 1
    if player.direct_move == walk_left:
        self.angle = 60
        try:
            player.isAttack = False
            screen.blit(player.weapon.attack_anim[player.weapon.attack_count], (player.pos_x - 30, player.pos_y))
            self.attack_count += 1
            rect = self.attack_anim[self.attack_count].get_rect()
            rect.x = player.pos_x - 30
            rect.y = player.pos_y
            return rect
        except:
            self.attack_count = 0
            self.angle = 0
            player.isAttack = True
            return 1

def katanAttackEf(self,zombie,player):
    zombie.health -= self.damage



def katanUltimate(self,screen,player,angle):
    x = player.pos_x
    y = player.pos_y

    if -90 <= angle <= 90:
        try:
            self.angle = 45
            rotated_img = pygame.transform.rotate(self.ultimate_anim[self.attack_count], -angle)
            rect = screen.blit(rotated_img, (x, y))
            self.attack_count += 1
            player.pos_x += 10 * math.cos(math.radians(angle))
            player.pos_y += 10 * math.sin(math.radians(angle))
            return rect
        except IndexError:
            self.attack_count = 0
            self.angle = 0
            return 1
    else:
        try:
            self.angle = 45
            rotated_img = pygame.transform.rotate(self.ultimate_anim[self.attack_count], -angle)
            rect = screen.blit(pygame.transform.flip(rotated_img, True, False), (x, y))
            self.attack_count += 1
            player.pos_x -= 10 * math.cos(math.radians(angle))
            player.pos_y -= 10 * math.sin(math.radians(angle))
            return rect
        except IndexError:
            self.attack_count = 0
            self.angle = 0
            return 1

def katanUltimateEf(self,zombie,player):
    zombie.health -= self.damage

