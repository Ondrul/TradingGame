import pygame as pg
import random
import time
import json
import os
import math
from data import stocks

pg.init()
font = pg.font.SysFont("arial", 40)
width, height = 1600, 900
win = pg.display.set_mode((width, height))
pg.display.set_caption("Trading Game")
clock = pg.time.Clock()

# Increase FPS for smoother animation
TARGET_FPS = 144

pozadi = pg.transform.scale(pg.image.load("pozadi.png"), (width, height))
start_img = pg.transform.scale(pg.image.load("start.png"), (width, height))
game_over_img = pg.transform.scale(pg.image.load("game_over.png"), (width, height))
survived_img = pg.transform.scale(pg.image.load("survived.png"), (width, height))
rich_img = pg.transform.scale(pg.image.load("rich.png"), (width, height))

sfx_pay = pg.mixer.Sound("paying.mp3")
sfx_money = pg.mixer.Sound("recieve_money.mp3")
sfx_gameover = pg.mixer.Sound("game_over_sound.mp3")
sfx_sfx = pg.mixer.Sound("game_sfx.mp3")

sfx_pay.set_volume(0.5)
sfx_money.set_volume(0.5)
sfx_gameover.set_volume(0.5)


with open('events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

state = "start"
money = 2000
stock = 0
stock_price = 0
profit = 0
rent = 0
total_cost = 0
realized_profit = 0
buy_discount = 1.0
sell_penalty = 1.0
market_open = True
event_count = 0
event_text = "Trh je normální"
input_text = "1"
total_money = 0
pay_amount = 0
sell_amount = 0

DEFAULT_PAY_COORDINATES_X = width // 10
DEFAULT_PAY_COORDINATES_Y = height // 10
DEFAULT_PAY_VELOCITY = 0

pay_coordinates_x = DEFAULT_PAY_COORDINATES_X
pay_coordinates_y = DEFAULT_PAY_COORDINATES_Y
pay_animation_velocity = DEFAULT_PAY_VELOCITY
pay_animation_color_buy = (255, 50, 50)
pay_animation_color_sell = (50, 255, 50)
pay_animation_color = pay_animation_color_buy

def scale(val, src, dst):
    return dst[0] + (float(val - src[0]) / (src[1] - src[0]) * (dst[1] - dst[0]))

def lerp(a, b, t):
    return a + (b - a) * t

current_segment = 0
pos_on_line = 0.0
animation_speed = 0.02

def draw_game():
    win.blit(pozadi, (0, 0))
    
    average_buy_price = total_cost / stock if stock > 0 else 0
    unrealized_profit = (stock_price - average_buy_price) * stock
    total_profit = realized_profit + unrealized_profit
    info = font.render(f"Peníze: {round(money)} $  Profit: {round(total_profit)} $  Akcie: {stock} ks   Cena: {round(stock_price)} $", True, (255, 255, 255))
    win.blit(info, (50, 50))

    event_width, event_height = 650, 55
    event_x = width - event_width - 75
    event_y = 50
    event_box = pg.Rect(event_x, event_y, event_width, event_height)
    pg.draw.rect(win, (50, 50, 50), event_box)
    pg.draw.rect(win, (200, 200, 200), event_box, 3)
    event_font = pg.font.SysFont("arial", 30)
    event = event_font.render(event_text, True, (255, 255, 255))
    win.blit(event, (event_x + 10, event_y + 12))

    digit_box = pg.Rect(700, 800, 200, 55)
    pg.draw.rect(win, (50, 50, 50), digit_box)
    pg.draw.rect(win, (200, 200, 200), digit_box, 3)
    input_display = font.render("Kolik: " + input_text, True, (255, 255, 255))
    win.blit(input_display, (710, 810))

    pg.draw.rect(win, (0, 255, 0), pg.Rect(1000, 800, 150, 50))
    buy_text = font.render("Koupit", True, (255, 255, 255))
    win.blit(buy_text, (1015, 805))

    pg.draw.rect(win, (255, 0, 0), pg.Rect(1200, 800, 150, 50))
    sell_text = font.render("Prodat", True, (255, 255, 255))
    win.blit(sell_text, (1215, 805))

    draw_graph()

def draw_graph():
    global current_segment, pos_on_line
    
    win.set_clip(pg.Rect(100, 250, 1300, 500))
    pg.draw.rect(win, (15, 15, 15), (100, 250, 1300, 500))
    
    grid_color = (30, 30, 30)
    for y in range(300, 701, 50):
        pg.draw.line(win, grid_color, (100, y), (1400, y), 1)
    for x in range(100, 1401, 100):
        pg.draw.line(win, grid_color, (x, 250), (x, 750), 1)
    
    if current_segment > 0 and len(points) > 1:
        completed_points = [(p[0] - scroll, p[1]) for p in points[:current_segment + 1]]
        if len(completed_points) >= 2:
            pg.draw.lines(win, (0, 255, 204), False, completed_points, 2)
    
    if current_segment < len(points) - 1:
        start = (points[current_segment][0] - scroll, points[current_segment][1])
        end = (points[current_segment + 1][0] - scroll, points[current_segment + 1][1])
        
        current_x = lerp(start[0], end[0], pos_on_line)
        current_y = lerp(start[1], end[1], pos_on_line)
        
        pg.draw.line(win, (0, 255, 204), start, (int(current_x), int(current_y)), 2)
        
        # Aktualizovat pozici
        pos_on_line += animation_speed
        if pos_on_line >= 1.0:
            pos_on_line = 0.0
            current_segment += 1
    
    win.set_clip(None)

def create_line(p1, p2, color=(0, 255, 204)):
    return {
        'start': p1,
        'end': p2,
        'color': color
    }

def popup_info(win, prompt, font):
    active = True
    width, height = win.get_size()
    box_width, box_height = 400, 100
    box_x = (width - box_width) // 2
    box_y = (height - box_height) // 2

    while active:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                active = False
        pg.draw.rect(win, (50, 50, 50), (box_x, box_y, box_width, box_height))
        pg.draw.rect(win, (200, 200, 200), (box_x, box_y, box_width, box_height), 3)
        prompt_surface = font.render(prompt, True, (255, 255, 255))
        win.blit(prompt_surface, (box_x + 20, box_y + box_height // 3))
        pg.display.flip()
        clock.tick(10)

def event_on():
    global buy_discount, sell_penalty, market_open, event_text
    choice_array = []
    for key in ["normal", "cheap_buy", "bad_sell", "market_closed", "black_friday"]:
        for _ in range(int(events[key]["chance"])):
            choice_array.append(key)
    choice = random.choice(choice_array)
    eventParameters = events[choice]
    buy_discount = eventParameters["buy_discount"]
    sell_penalty = eventParameters["sell_penalty"]
    market_open = eventParameters["market_open"]
    event_text = eventParameters["event_text"]

lines = []
scroll = 0
scroll_speed = 3
points_per_tick = 12

def main():
    global state, money, stock, stock_price, profit, rent, total_cost, realized_profit
    global buy_discount, sell_penalty, market_open, event_count, event_text, input_text
    global total_money, day_index, points, lines, scroll
    global last_update, last_rent_time, last_event_time, game_start_time
    global current_segment, pos_on_line

    running = True
    day_index = 0
    company_name, company_data = random.choice(list(stocks.items()))
    close_prices = company_data["Close"].values.copy()
    stock_price = round(float(close_prices[0]))
    data_min, data_max = min(close_prices), max(close_prices)
    points = [(250, int(scale(stock_price, (data_min, data_max), (700, 300))))]
    lines = []
    scroll = 0
    current_segment = 0
    pos_on_line = 0.0
    
    last_update = time.time()
    last_rent_time = time.time()
    last_event_time = time.time()
    game_start_time = time.time()

    while running:
        frame_start = time.time()
        clock.tick(TARGET_FPS)
        current_time = time.time()
        win.blit(pozadi, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if state == "start" and event.type == pg.MOUSEBUTTONDOWN:
                sfx_sfx.play()
                sfx_sfx.set_volume(0.1)
                state = "game"
                game_start_time = current_time
            if state == "game" and event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit():
                    input_text += event.unicode
            if state == "game" and event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                price = round(float(close_prices[day_index]))
                stock_price = price
                if 1000 <= x <= 1150 and 800 <= y <= 850:
                    if market_open:
                        if input_text.isdigit() and int(input_text) > 0:
                            how_much = int(input_text)
                            total_cost_of_buy = price * how_much * buy_discount
                            if money >= total_cost_of_buy:
                                stock += how_much
                                money -= total_cost_of_buy
                                total_cost += price * how_much
                                sfx_pay.play()
                                pay_amount = int(total_cost_of_buy)
                                input_text = "1"
                            else:
                                popup_info(win, "Nemáš dostatek peněz", font)
                        else:
                            popup_info(win, "Napiš prosím platné číslo", font)
                    else:
                        popup_info(win, "Dnes je zavřený trh. Nemůžeš nakupovat.", font)
                elif 1200 <= x <= 1350 and 800 <= y <= 850:
                    if market_open:
                        if input_text.isdigit() and int(input_text) > 0:
                            how_much = int(input_text)
                            if stock >= how_much:
                                average_buy_price = total_cost / stock if stock > 0 else 0
                                stock -= how_much
                                money += price * how_much * sell_penalty
                                total_cost -= average_buy_price * how_much
                                sell_amount = price * how_much * sell_penalty
                                sfx_money.play()
                                input_text = "1"
                            else:
                                popup_info(win, "Nemáš dostatek akcií", font)
                        else:
                            popup_info(win, "Napiš prosím platné číslo", font)
                    else:
                        popup_info(win, "Dnes je zavřený trh. Nemůžeš prodávat.", font)

            if (state == "over" or state == "end") and event.type == pg.MOUSEBUTTONDOWN:
                state = "start"
                money = 2000
                stock = 0
                stock_price = 0
                profit = 0
                rent = 0
                total_cost = 0
                realized_profit = 0
                buy_discount = 1.0
                sell_penalty = 1.0
                market_open = True
                event_count = 0
                event_text = "Trh je normální"
                input_text = "1"
                total_money = 0
                day_index = 0
                
                company_name, company_data = random.choice(list(stocks.items()))
                close_prices = company_data["Close"].values.copy()
                stock_price = round(float(close_prices[0]))
                points = [(250, int(scale(stock_price, (data_min, data_max), (700, 300))))]
                lines = []
                scroll = 0
                
                last_update = current_time
                last_rent_time = current_time
                last_event_time = current_time
                game_start_time = current_time

        if state == "game":
            if current_time - game_start_time > 300:
                state = "end"


            if current_time - last_update > 0.2 and day_index < len(close_prices) - 1:
                day_index += 1
                stock_price = round(float(close_prices[day_index]))
                x = points[-1][0] + points_per_tick
                y = scale(stock_price, (data_min, data_max), (700, 300))
                new_point = (x, int(y))
                points.append(new_point)
                last_update = current_time

            if points[-1][0] - scroll > 1200:
                scroll += 1

            if current_time - last_event_time > 15:
                event_on()
                last_event_time = current_time

            if current_time - last_rent_time > 20:
                if money < 100:
                    state = "over"
                else:
                    money -= 100
                    rent += 1
                last_rent_time = current_time

            draw_game()

        elif state == "start":
            win.blit(start_img, (0, 0))
        elif state == "over":
            win.blit(game_over_img, (0, 0))
            sfx_gameover.play()
        elif state == "end":
            total_money = money + round(float(close_prices[day_index]))
            if total_money <= 1999:
                win.blit(survived_img, (0, 0))
            elif 2000 <= total_money < 3999:
                win.blit(game_over_img, (0, 0))
            elif total_money >= 4000:
                win.blit(rich_img, (0, 0))

        pg.display.update()

        frame_time = time.time() - frame_start
        if frame_time < 1.0/TARGET_FPS:
            pg.time.wait(int((1.0/TARGET_FPS - frame_time) * 1000))

    pg.quit()

if __name__ == "__main__":
    main()
