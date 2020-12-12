import pygame as pg
import random
import json
pg.init()


display_width = 900
display_height = 600
display = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('Бегите, глупцы!')

user_width = 60
user_height = 100
user_x = display_width // 3
user_y = display_height - 100 - user_height

count = 0  #считает картинки дрыгания ногами динозавра
clock = pg.time.Clock()
jump_counter = 25
change_speed = 90
make_jump = False
score = 0
more_than = 50 #минимальное количество очков для продолжения игры

dino_img = [ pg.image.load('Dino2_' + str(i) + '.png') for i in range(5)]
land = pg.image.load('задний фон.png')
cuc3 = pg.image.load('Толстый кактус.png')


class Cuctus():
    def __init__(self, x, y, width, height, image = ''):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.image = image
        self.speed = 5
        self.score = 1
        self.min_distance = 400

    def draw_cuctus(self):
        if self.x + self.width > 0:
            if self.image != '':
                display.blit(self.image,(self.x,self.y))
            else:
                pg.draw.rect(display, (50, 250, 50), (self.x, self.y, self.width, self.height))

            self.x -= self.speed

        else:
            maximum = max(cuctus_arr[0].x, cuctus_arr[1].x, cuctus_arr[2].x)
            distanse = display_width - maximum

            if distanse < self.min_distance:
                self.x = display_width + self.width + (self.min_distance - distanse) + random.randrange(-100,200)
                self.score += 1
            else:
                self.x = display_width + self.width
                self.score += 1
            count_plus = 10 #на сколько уведичивать расстояние
            if self.score % 2 == 0:
                self.speed += 2
                self.x += 400
                self.min_distance += self.score * count_plus
                count_plus += 10



cuctus1 = Cuctus(display_width + 50, display_height - 100 - 140, 30, 140, )
cuctus2 = Cuctus(display_width + 360, display_height - 100 - 80, 85, 80)
cuctus3 = Cuctus(display_width + 700, display_height - 100 - 110, 45, 110)
cuctus_arr = [cuctus1, cuctus2, cuctus3]
cuctus_x_pos = [display_width , display_width + 200 * cuctus_arr[0].speed, display_width + 400 * cuctus_arr[0].speed]




def draw_arr(array): #рисует все кактусы
    for cuctus in array:
        cuctus.draw_cuctus()

def is_collision(): #проверка на столкновение
    for cuctus in cuctus_arr:
        if (user_y + user_height > cuctus.y) and (user_x + user_width > cuctus.x) and (user_x + user_width < cuctus.x + cuctus.width):
            return True
        if (user_y + user_height > cuctus.y) and (user_x > cuctus.x) and (user_x < cuctus.x + cuctus.width):
            return True

def run_game():
    global make_jump, score
    game = True
    while game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            pause()
        if keys[pg.K_SPACE]:
            make_jump = True
        if make_jump:
            jump()


        display.blit(land,(0,0))
        draw_arr(cuctus_arr)
        draw_dino()

        count_score()
        string = 'Ваш счёт: ' + str(score)
        print_text(string, 10 , 10 , (0,0,0), 10)

        if is_collision():
            game = False
            game_over()


        pg.display.update()
        clock.tick(60)

def pause():
    flag = True
    while flag:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        print_text('Пауза',300, 200, (0,0,0) , 50)
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            flag = False
        pg.display.update()

def start_game():
    while True:
        print_text('''Нажми [f5], чтобы начать''',200,200,(255,255,255), 20)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            keys = pg.key.get_pressed()
            if keys[pg.K_F5]:
                run_game()


def game_over():
    global user_y, more_than

    new_record = False
    with open('currency.json', 'r') as file:
        load_currency = json.load(file)
    maximum = max(load_currency['record'])
    load_currency['all_points'] += score
    if score > maximum:
        load_currency['record'].append(score)
    with open('currency.json', 'w') as file:
        json.dump(load_currency, file)
    if load_currency['record'][-1] > maximum:
        new_record = True

    while True:
        print_text('Игра окончена.',150,150,(0,0,0), 50)
        print_text(f'-{more_than} валюты, чтобы продолжить [f5]', 150, 230, (0, 0, 0), 20)
        print_text('ай, блин, больно(((', user_x - 5, user_y - 10, (0,0,0), 10)
        print_text('Всего валюты:' + str(load_currency['all_points']), 700, 10, (0,0,0), 10 )
        if new_record:
            print_text('Новый рекорд!', 200, 50, (100, 100, 100), 30)


        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        keys = pg.key.get_pressed()
        if keys[pg.K_F5]:
            if load_currency['all_points'] >= more_than:
                load_currency['all_points'] -= more_than
                with open('currency.json', 'w') as file:
                    json.dump(load_currency, file)
                more_than = more_than * 2
                m = cuctus_arr[0].speed
                for i in range(3):
                    cuctus_arr[i].x = cuctus_x_pos[i]
                    cuctus_arr[i].speed = m
                run_game()



def jump():
    global user_y, jump_counter, make_jump, count
    if jump_counter >= -25:
        user_y -= jump_counter
        jump_counter -= 1
    else:
        jump_counter = 25
        make_jump = False
    #не дрыгать ногами во время прыжка
    count-= 1

def draw_dino(): #анимирует динозаврика
    global count, change_speed


    if count == change_speed:
        count = 0
        if change_speed != 10:
            change_speed -= 5
    change_pictures = count // (int(change_speed/5))
    if change_speed // 5 == 1:
        change_pictures = count
    display.blit(dino_img[change_pictures], (user_x, user_y))
    count += 1

def print_text(print, x, y, color, size):
    font_type = pg.font.Font('PressStart2P-Regular.ttf', size)
    text = font_type.render(print, True, color)
    display.blit(text, (x,y))

def count_score():
    global score
    for i in cuctus_arr:
        if  i.x - i.speed < user_x < i.x + 1:
            score += 1

start_game()