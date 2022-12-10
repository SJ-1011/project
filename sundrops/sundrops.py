import pygame, sys, random
from pygame.locals import QUIT
from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT
pygame.init()
display_surface = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("My project")
background_sound = pygame.mixer.Sound('sound/background.mp3')
grow_sound = pygame.mixer.Sound('sound/grow.mp3')



class button(pygame.sprite.Sprite):
    def __init__(self,num,x,y):
        super().__init__()
        if num == 1:
            self.image = pygame.image.load('image/menu_start.png')
        if num == 2:
            self.image = pygame.image.load('image/menu_way.png')          
        if num == 3:
            self.image = pygame.image.load('image/menu_exit.png')       
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.bottom = y

class fall(pygame.sprite.Sprite):
    def __init__(self,num,x,y):
        super().__init__()
        if num == 1:
            self.image = pygame.image.load('image/fire.png')
        if num == 2:
            self.image = pygame.image.load('image/heart.png')          
        if num == 3:
            self.image = pygame.image.load('image/water.png')       
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.bottom = y

class point(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([1,1], pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.x = pygame.mouse.get_pos()[0]
        self.rect.y = pygame.mouse.get_pos()[1]
        
        
def change_sundrops_image(num = 0):
    if num == 0:
        sundrops_image = pygame.image.load("image/seed.png")
    if num == 1:
        sundrops_image = pygame.image.load("image/sprout.png")
    if num == 2:
        sundrops_image = pygame.image.load("image/stem.png")  # 이미지 바꾸기 큰 줄기
    if num == 3:
        sundrops_image = pygame.image.load("image/flower.png") # 이미지 바꾸기 꽃 그림
    sundrops_rect = sundrops_image.get_rect()
    return sundrops_image, sundrops_rect, num + 10

def change_background(num = 0):
    if num == 0:
        return pygame.image.load('image/project_background.png')
    if num == 1:
        return pygame.image.load('image/project_background1.png')
    if num == 2:
        return pygame.image.load('image/project_background2.png')
    if num == 3:
        return pygame.image.load('image/project_background3.png')
    if num == 4:
        return pygame.image.load("image/project_background0.png")
    if num == 5:
        return pygame.image.load('image/game_rule.png')
    
def play_sound(num):
    if num == 0:
        background_sound.play()
        
def final(num):
    if num == 0:
        display_surface.blit(pygame.image.load('image/over.png'), (0, 0))
        
    if num == 1:
        display_surface.blit(pygame.image.load('image/win.png'), (0, 0))
                    
def main():
    # 달맞이꽃 객체 생성
    sundrops_image, sundrops_rect, k = change_sundrops_image()
    sundrops_rect.centerx = 500
    sundrops_rect.bottom = 670
    
    fire = fall(1, random.randint(50, 950), random.randint(-1000, -100))
    fire2 = fall(1, random.randint(50, 950), random.randint(-1000, -100))
    heart = fall(2, random.randint(50, 950), random.randint(-1000, 0))
    water = fall(3, random.randint(50, 950), random.randint(-5000, -3000))
    # 버튼 객체 생성
    start_bt = button(1,500,400)
    rule_bt = button(2,500,480)
    exit_bt = button(3,500,560)
    
    
    FPSCLOCK = pygame.time.Clock()
    

    sysfont = pygame.font.SysFont(None, 50, True)
    life_num = 5
    score_num = 0
    a = 0
    
    background_num = 4
    
    while True:
        if background_num == 4 or background_num == 5:
            display_surface.blit(change_background(background_num), (0, 0))
            
            display_surface.blit(start_bt.image, start_bt.rect)
            display_surface.blit(rule_bt.image, rule_bt.rect)
            display_surface.blit(exit_bt.image, exit_bt.rect)
            
            po = point()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()
                po.update()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if(pygame.sprite.collide_rect(po, start_bt)): 
                        background_num = 0
                    if(pygame.sprite.collide_rect(po, rule_bt)): 
                        background_num = 5
                        start_bt.rect.x = 270
                        start_bt.rect.y = 580
                        rule_bt.rect.x = -100
                        rule_bt.rect.y = -100
                        exit_bt.rect.x = 590
                        exit_bt.rect.y = 580
                    if(pygame.sprite.collide_rect(po, exit_bt)): 
                        pygame.quit()
                        sys.exit()
                
            
            FPSCLOCK.tick(50)
            pygame.display.update()
        
        else:
            play_sound(a)
            a = 1
            
            display_surface.blit(change_background(background_num), (0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()
                    
            # 애정 획득시
            if sundrops_rect.colliderect(heart.rect):
                score_num += 1
                heart.rect.x = random.randint(50, 950)
                heart.rect.y = random.randint(-1000, 0)
            
            # 애정 피하면? 재생성
            if heart.rect.y > 1000:
                heart.rect.x = random.randint(50, 950)
                heart.rect.y = random.randint(-1000, 0)
            
            # 불 획득시
            if sundrops_rect.colliderect(fire.rect):
                life_num -= 1
                fire.rect.x = random.randint(50, 950)
                fire.rect.y = random.randint(-1000, -100)
                
            # 불 피하면? 재생성
            if fire.rect.y > 1000:
                fire.rect.x = random.randint(50, 950)
                fire.rect.y = random.randint(-1000, 0)
                
            # 불2 획득시
            if sundrops_rect.colliderect(fire2.rect):
                life_num -= 1
                fire2.rect.x = random.randint(50, 950)
                fire2.rect.y = random.randint(-1000, -100)
                
            # 불2 피하면? 재생성
            if fire2.rect.y > 1000:
                fire2.rect.x = random.randint(50, 950)
                fire2.rect.y = random.randint(-1000, 0)
                
            # 물 획득시
            if sundrops_rect.colliderect(water.rect):
                score_num += 3
                water.rect.x = random.randint(50, 950)
                water.rect.y = random.randint(-5000, -3000)
                
            # 물 피하면? 재생성
            if water.rect.y > 1000:
                water.rect.x = random.randint(50, 950)
                water.rect.y = random.randint(-5000, -3000)
            
            # 새싹으로 성장, 이 밑으로 score 범위 5<_<10 이런식으로 바꾸기
            if (score_num >= 3 and score_num < 10) and k != 11:
                grow_sound.play()
                sundrops_image, sundrops_rect, k = change_sundrops_image(1)
                sundrops_rect.centerx = 500
                sundrops_rect.bottom = 680
                background_num += 1
            
            # 큰 줄기로 성장
            if (score_num >= 10 and score_num < 20) and k != 12:
                grow_sound.play()
                sundrops_image, sundrops_rect, k = change_sundrops_image(2)
                sundrops_rect.centerx = 500
                sundrops_rect.bottom = 680
                background_num += 1
            
            # 꽃 피우기
            if (score_num >= 20) and k != 13:
                grow_sound.play()
                sundrops_image, sundrops_rect, k = change_sundrops_image(3)
                sundrops_rect.centerx = 500
                sundrops_rect.bottom = 680
                background_num += 1
            
            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_LEFT]:
                    sundrops_rect.x -= 20
                if  keys[K_RIGHT]:
                    sundrops_rect.x += 20
            
            heart.rect.y += 15
            fire.rect.y += 15
            water.rect.y += 24
            fire2.rect.y += 20
            
            display_surface.blit(sundrops_image, sundrops_rect)
            display_surface.blit(heart.image, heart.rect)
            display_surface.blit(fire.image, fire.rect)
            display_surface.blit(water.image, water.rect)
            display_surface.blit(fire2.image, fire2.rect)
            
            
            life = sysfont.render(f"Life: {life_num}", True, (0, 0, 0))
            life_rect = life.get_rect()
            life_rect.topleft = (30, 30)
            display_surface.blit(life, life_rect)
            
            score = sysfont.render(f"Score: {score_num}", True, (0, 0, 0))
            score_rect = score.get_rect()
            score_rect.topleft = (30, 80)
            display_surface.blit(score, score_rect)
            
            if life_num <= 0:
                final(0)
                sundrops_rect.centerx = 5000
                sundrops_rect.bottom = 5000
            
            if score_num >= 30:
                final(1)
                sundrops_rect.centerx = 5000
                sundrops_rect.bottom = 5000
            
            
            FPSCLOCK.tick(50)
            pygame.display.update()
            
                

if __name__ == '__main__':  
    main()
