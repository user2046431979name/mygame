import math
import random

import pygame.transform
from requier import *



pygame.init()

display_size = (600,400)
clock = pygame.time.Clock()
fps = 30
pygame.display.set_caption("Zerot")

screen = pygame.display.set_mode(display_size)

world_bg1 = pygame.surface.Surface((1914,836))
world_bg2 = pygame.image.load('images/background1.png').convert()


scale = 2
world_size = (1914,836)
scaled_display_size = (display_size[0] // scale, display_size[1] // scale)




def TransformScale(obj,f,s):
    return pygame.transform.scale(obj,(f,s))

def TransformRotate(obj,f):
    return pygame.transform.rotate(obj,f)

class Player:
    def __init__(self,pos_x,pos_y,anim_count,direct_move,player_speed,health,weapon):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = direct_move[anim_count].get_rect()
        self.anim_count = anim_count
        self.player_speed = player_speed
        self.direct_move = direct_move
        self.health = health
        self.weapon = weapon
        self.isAttack = True

    def animation(self):
        if self.anim_count == 3:
            self.anim_count = 0
        self.anim_count += 1




class Bullet:
    def __init__(self,pos_x,pos_y,angle,image,bullet_speed):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.angle = angle
        self.image = image
        self.rect = image.get_rect()
        self.bullet_speed = bullet_speed
    def update(self):
        self.pos_x += self.bullet_speed * math.cos(math.radians(self.angle))
        self.pos_y += self.bullet_speed * math.sin(math.radians(self.angle))

    def draw(self,screen):
        rotated_bullet = pygame.transform.rotate(self.image, -self.angle)
        screen.blit(TransformScale(rotated_bullet, 10, 5), (self.pos_x, self.pos_y))





class Zombie:
    def __init__(self,pos_x,pos_y,health,damage,direct_move,anim_count,speed,name):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.health = health
        self.max_health = health
        self.damage = damage
        self.direct_move = direct_move
        self.anim_count = anim_count
        self.rect = direct_move[anim_count].get_rect()
        self.speed = speed
        self.name = name
        self.last_animation_time = pygame.time.get_ticks()
        self.animation_interval = 200


    def update(self, player_rect):
        dx = player_rect.x - self.rect.x
        dy = player_rect.y - self.rect.y
        dist = math.hypot(dx, dy)

        if dist != 0:
            move_x = dx / dist * self.speed
            move_y = dy / dist * self.speed


            self.pos_x += move_x
            self.pos_y += move_y


            self.rect.x = self.pos_x
            self.rect.y = self.pos_y


            if pygame.time.get_ticks() - self.last_animation_time > self.animation_interval:
                if self.anim_count == 2:
                    self.anim_count = 0
                else:
                    self.anim_count += 1
                self.last_animation_time = pygame.time.get_ticks()

            if move_x < 0:
                self.direct_move = z_left
            elif move_x > 0:
                self.direct_move = z_right

    def attack(self,player):
        if pygame.time.get_ticks() - self.last_animation_time > self.animation_interval:
            if self.anim_count == 5:
                self.anim_count = 0
            else:
                self.anim_count += 1

            player.health -= self.damage
            self.last_animation_time = pygame.time.get_ticks()


class Sword:
    def __init__(self,image,damage,attack_anim,attack_sound,combo_attack_time,attack_time,attack_func,ultimate_func,attack_ef,ultimate_ef):
        self.image = image
        self.rect = image.get_rect()
        self.damage = damage
        self.attack_anim = attack_anim[0]
        self.ultimate_anim = attack_anim[1]
        self.attack_count = 0
        self.angle = 0
        self.attack_sound = attack_sound
        self.combo_attack_time = combo_attack_time
        self.attack_time = attack_time
        self.isCombo = False
        self.attack_func = attack_func
        self.ultimate_func = ultimate_func
        self.attack_ef = attack_ef
        self.ultimate_ef = ultimate_ef
    def draw(self,screen,player):
        if player.direct_move == walk_right:
           rotated_img = TransformRotate(self.image,self.angle)
           screen.blit(pygame.transform.flip(rotated_img,True,False),(player.pos_x,player.pos_y))
        elif player.direct_move == walk_left:
           rotated_img = TransformRotate(self.image,self.angle)
           screen.blit(pygame.transform.flip(rotated_img, False, False), (player.pos_x - 20, player.pos_y))

    def attack(self,screen,player):
        rect = self.attack_func(self,screen,player)
        return rect

    def ultimate_skill(self,screen,player,angle):
        rect = self.ultimate_func(self,screen,player,angle)
        return rect


class Slash:
    def __init__(self,damage,weapon,isUltimate):
        self.damage = damage
        self.weapon = weapon
        self.isUltimate = isUltimate
        self.start_time = pygame.time.get_ticks()
    def attack(self,screen,player,angle):
        if self.isUltimate:
            rect = player.weapon.ultimate_skill(screen,player,angle)
            return rect
        else:
            rect = player.weapon.attack(screen,player)
            return rect
    def attack_ef(self,zombie,player):
        if self.isUltimate:
            self.weapon.ultimate_ef(self,zombie,player)
        else:
            self.weapon.attack_ef(self,zombie,player)






katana = Sword(katana_img,50,slash_katana,[katana_no_hit_sounds,katana_hit_sounds],2000,500,katanAttack,katanUltimate,katanAttackEf,katanUltimateEf)



player = Player(130,80,0,walk_right,5,100,katana)



zombie_timer = pygame.USEREVENT + 1
pygame.time.set_timer(zombie_timer,random.randint(3000,10000))



camera_x = 0
camera_y = 0


restart = system_font.render("restart?", True, (0, 0, 0))
quit = system_font.render("quit?", True, (0, 0, 0))

restart_rect = restart.get_rect(topleft=(190,160))
quit_rect = quit.get_rect(topleft=(190,220))

running = True
gameplay = True

slashes_list = []


bullets_list = []

zombie_list = []




last_time = pygame.time.get_ticks()

frame_time = 500

kills = 0

while running:



    if gameplay:
        player.rect.x = player.pos_x
        player.rect.y = player.pos_y




        s_world1 = TransformScale(world_bg1,world_size[0] * 2,world_size[1] * 2)


        screen.fill((0, 0, 0))
        screen.blit(s_world1, (camera_x, camera_y))

        player_img = player.direct_move[player.anim_count]


        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        current_time = pygame.time.get_ticks()

        start_pos = (player.pos_x + 10, player.pos_y + 10)
        end_pos = ((player.pos_x - 130) + mouse_x / 2,(player.pos_y - 80) + mouse_y / 2)

        player_center_x = player.pos_x + player_img.get_width() // 2
        player_center_y = player.pos_y + player_img.get_height() // 2
        angle = math.atan2(((player.pos_y - 80) + mouse_y / 2) - player_center_y,((player.pos_x - 130) + mouse_x / 2) - player_center_x)
        angle_degrees = math.degrees(angle)

        if keys[pygame.K_d]:
            player.pos_x += player.player_speed

            player.direct_move = walk_right
            player.animation()
        if keys[pygame.K_a]:
            player.pos_x -= player.player_speed


            player.direct_move = walk_left
            player.animation()

        if keys[pygame.K_w]:
            player.animation()
            player.pos_y -= player.player_speed



        if keys[pygame.K_s]:
            player.animation()
            player.pos_y += player.player_speed




        camera_x -= (player.pos_x - 130) + camera_x / 2
        camera_y -= (player.pos_y - 80) + camera_y / 2



        world_bg1.blit(player_img, (player.pos_x, player.pos_y))
        world_bg1.fill((0, 0, 0))
        world_bg1.blit(world_bg2, (0, 0))
        world_bg1.blit(player_img, (player.pos_x, player.pos_y))




        if zombie_list:
            for zombie in zombie_list:
                try:
                    z_img = zombie.direct_move[zombie.anim_count]
                except:
                    zombie.anim_count = 0
                    z_img = zombie.direct_move[zombie.anim_count]
                world_bg1.blit(TransformScale(z_img,40,40),(zombie.pos_x,zombie.pos_y))
                zombie.update(player.rect)





                if zombie.health <= 0:
                    zombie_list.remove(zombie)
                    kills += 1





                if zombie.rect.colliderect(player.rect) and player.isAttack and pygame.time.get_ticks() - last_time >= 300:
                    zombie.attack(player)
                try:
                    zombie_health_precent = (zombie.health * 100)//zombie.max_health
                    zombie_health = (30 * zombie_health_precent) // 100
                    zombie_health_l = pygame.surface.Surface((zombie_health, 5))
                    zombie_health_l.fill((0, 255, 0))
                    world_bg1.blit(zombie_health_l, (zombie.pos_x, zombie.pos_y + 1))
                except:
                    continue

        player.weapon.rect.x,player.weapon.rect.y = player.rect.centerx,player.rect.centery
        player.weapon.draw(world_bg1,player)

        if slashes_list:
            for i in slashes_list:
                current_time = pygame.time.get_ticks()
                if current_time - last_time >= 100:
                    rect = i.attack(world_bg1,player,angle_degrees)
                    if rect == 1:
                        slashes_list.remove(i)
                    else:
                        pygame.draw.rect(world_bg1,(255,0,0),rect,1)
                        if zombie_list:
                            for z in zombie_list:
                                if rect.colliderect(z.rect):
                                    i.attack_ef(z,player)

                    last_time = current_time







        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == zombie_timer:
                zombie = Zombie(pos_x=random.randint(0,1000), pos_y=random.randint(0,800), health=random.randint(100,500), damage=random.randint(5,10), direct_move=z_right,anim_count=0, speed=2, name='zombie(normal)')
                zombie_list.append(zombie)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_d or event.key == pygame.K_a:
                    player.anim_count = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_time = pygame.time.get_ticks()
                    player.weapon.isCombo = True



            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if pygame.time.get_ticks() - start_time >= player.weapon.combo_attack_time:

                        slash = Slash(damage=player.weapon.damage * 2, weapon=player.weapon, isUltimate=True)
                        slashes_list.append(slash)
                    else:
                        if pygame.time.get_ticks() - last_time >= 100:
                           slash = Slash(damage=player.weapon.damage, weapon=player.weapon, isUltimate=False)
                           slashes_list.append(slash)
                    player.weapon.isCombo = False





        if player.weapon.isCombo and mouse_buttons[0]:
            player.weapon.damage += player.weapon.damage * 2

            label_w = (30 * (((pygame.time.get_ticks() - start_time) * 100) // player.weapon.combo_attack_time)) // 100
            label_w = 30 if label_w > 30 else label_w
            ulta_label = pygame.surface.Surface((label_w + 1,5))
            ulta_label.fill((255,255,255))



            if -90 <= angle_degrees <= 90:
                player.direct_move = walk_right
            else:
                player.direct_move = walk_left


            world_bg1.blit(ulta_label,(player.pos_x,player.pos_y))


        if player.health <= 0:
            gameplay = False


        try:
            health_label = pygame.surface.Surface((player.health + 1,15))
        except:
            health_label = pygame.surface.Surface((1,15))

        death_count = info_user_font.render(f"kills {kills}",True,(255,255,255))

        health_label.fill((255,0,0))
        screen.blit(health_label,(0,30))
        screen.blit(death_count,(0,0))
    else:
        screen.fill((255,0,0))
        death_label = system_font.render("You die",True,(0,0,0))





        screen.blit(death_label,(220,70))
        screen.blit(restart,restart_rect)
        screen.blit(quit,quit_rect)

        mouse = pygame.mouse.get_pos()

        if restart_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            player.pos_x = 130
            player.pos_y = 80

            gameplay = True
            camera_y = 0
            camera_x = 0
            player.health = 100

            bullets_list.clear()
            zombie_list.clear()


        if quit_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            run = False
            pygame.quit()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)



