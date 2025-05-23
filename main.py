import pygame as pg
import matplotlib.pyplot as plt
import random
import time
from data import stocks
import json


state = "start"
money = 2000
stock = 0
stock_price = 125.50
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

DEFAULT_PAY_COORDINATES_X = 160
DEFAULT_PAY_COORDINATES_Y = 100 
DEFAULT_PAY_VELOCITY = 0

pay_coordinates_x = DEFAULT_PAY_COORDINATES_X
pay_coordinates_y = DEFAULT_PAY_COORDINATES_Y
pay_animation_velocity = DEFAULT_PAY_VELOCITY
pay_animation_color_buy = (255, 50, 50)
pay_animation_color_sell = (50, 255, 50)
pay_animation_color = pay_animation_color_buy

pg.init()
font = pg.font.SysFont("arial", 40)
weight, height = 1800, 1000
win = pg.display.set_mode((weight, height))
pg.display.set_caption("Trading Game")
pozadi = pg.transform.scale(pg.image.load("pozadi.png"), (weight, height))
start_img = pg.transform.scale(pg.image.load("start.png"), (weight, height))
game_over = pg.transform.scale(pg.image.load("game_over.png"), (weight, height))
rich = pg.transform.scale(pg.image.load("rich.png"), (weight, height))
survived = pg.transform.scale(pg.image.load("survived.png"), (weight, height))
profit = pg.transform.scale(pg.image.load("profit.png"), (weight, height))
with open('events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)
buy_sfx = pg.mixer.Sound("paying.mp3")
sell_sfx = pg.mixer.Sound("recieve_money.mp3")
lose_sfx = pg.mixer.Sound("game_over_sound.mp3")
game_sfx = pg.mixer.Sound("game_sfx.mp3")

def generate_graph(data, day, name):
    plt.style.use('dark_background')
    plt.figure(figsize=(12, 5))
    plt.plot(data["Date"][:day], data["Close"][:day], color="#00FFCC")
    plt.title(f"Vývoj ceny akcie: {name}", color="white")
    plt.xlabel("Datum", color="white")
    plt.ylabel("Cena", color="white")
    plt.xticks(rotation=45, color="white")
    plt.yticks(color="white")
    plt.grid(color='#004444', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("graf.png", facecolor='#0d1117')
    plt.close()

def render_graph(win):
    graf = pg.image.load("graf.png")
    graf = pg.transform.scale(graf, (1200, 500))
    win.blit(graf, (250, 250))

def draw_start():
    win.blit(start_img, (0, 0))
    pg.display.update()

def start_pay_animation(is_buy):
    global pay_coordinates_x, pay_coordinates_y, pay_animation_velocity, pay_animation_color
    
    pay_coordinates_x = DEFAULT_PAY_COORDINATES_X
    pay_coordinates_y = DEFAULT_PAY_COORDINATES_Y
    pay_animation_velocity = 1
    if is_buy:
        pay_animation_color = pay_animation_color_buy
    else:
        pay_animation_color = pay_animation_color_sell

def update_pay_animation():
    global pay_coordinates_x, pay_coordinates_y, pay_animation_velocity, pay_animation_color
    if pay_animation_velocity > 0:
        pay_coordinates_y += pay_animation_velocity
        pay_text = font.render(f"-{pay_amount} $", True, pay_animation_color)
        win.blit(pay_text, (pay_coordinates_x, pay_coordinates_y))

    if pay_coordinates_y > 175:
        pay_animation_velocity = 0

def draw_game():
    global input_text, pay_amount, frame_count, frame_count_2, frame_count_3, frame_count_4, sell_amount, sell_frame_count, sell_frame_count_2, sell_frame_count_3, sell_frame_count_4, pay_coordinates_x, pay_coordinates_y,pay_animation_velocity
    win.blit(pozadi, (0, 0))
    average_buy_price = total_cost / stock if stock > 0 else 0
    unrealized_profit = (stock_price - average_buy_price) * stock
    total_profit = realized_profit + unrealized_profit

    info = font.render(f"Peníze: {round(money)} $  Profit: {round(total_profit)} $  Akcie: {stock} ks   Cena: {round(stock_price)} $", True, (255, 255, 255))
    win.blit(info, (50, 50))

    event_width, event_height = 650, 55
    event_x = weight - event_width - 75
    event_y = 50
    event_box = pg.Rect(event_x, event_y, event_width, event_height)
    pg.draw.rect(win, (50, 50, 50), event_box)
    pg.draw.rect(win, (200, 200, 200), event_box, 3)
    
    event_font = pg.font.SysFont("arial", 30)
    event = event_font.render(event_text, True, (255, 255, 255))
    win.blit(event, (event_x + 10, event_y + 12))

    update_pay_animation()    

    digit_width, digit_height = 200, 55
    digit_x = 700
    digit_y = 800
    digit_box = pg.Rect(digit_x, digit_y, digit_width, digit_height)
    pg.draw.rect(win, (50, 50, 50), digit_box)
    pg.draw.rect(win, (200, 200, 200), digit_box, 3)

    input_display = font.render("Kolik: " + input_text, True, (255, 255, 255))
    win.blit(input_display, (digit_x + 10, digit_y + 10))

    pg.draw.rect(win, (0, 255, 0), pg.Rect(1000, 800, 150, 50))
    buy_text = font.render("Koupit", True, (255, 255, 255))
    win.blit(buy_text, (1015, 805))

    pg.draw.rect(win, (255, 0, 0), pg.Rect(1200, 800, 150, 50))
    sell_text = font.render("Prodat", True, (255, 255, 255))
    win.blit(sell_text, (1215, 805))

    render_graph(win)
    pg.display.update()

def draw_survived():
    win.blit(survived, (0, 0))
    pg.display.update()

def draw_profit():
    win.blit(profit, (0, 0))
    pg.display.update()

def draw_rich():
    win.blit(rich, (0, 0))
    pg.display.update()

def draw_game_over():
    win.blit(game_over, (0, 0))
    pg.display.update()

def popup_info(win, prompt, font):
    global clock
    active = True
    clock = pg.time.Clock()
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
        for i in range(int(events[key]["chance"])):
            choice_array.append(key)

    choice = random.choice(choice_array)

    eventParameters = events[choice]
    buy_discount = eventParameters["buy_discount"]
    sell_penalty = eventParameters["sell_penalty"]
    market_open = eventParameters["market_open"]
    event_text = eventParameters["event_text"]
   


def main():
    global state, stock_price, profit, rent, money, stock, total_cost, realized_profit
    global event_count, buy_discount, sell_penalty, market_open, input_text, total_money
    global pay_amount, frame_count, frame_count_2, frame_count_3, frame_count_4, sell_amount
    global sell_frame_count, sell_frame_count_2, sell_frame_count_3, sell_frame_count_4

    run = True
    day_index = 45
    last_update = time.time()
    last_rent_time = time.time()
    last_event_time = time.time()
    game_start_time = time.time()

    company_name, company_data = random.choice(list(stocks.items()))
    stock_price = round(float(company_data["Close"].iloc[day_index]))
    generate_graph(company_data, day_index, company_name)

    while run:
        current_time = time.time()

        if state == "game" and (current_time - game_start_time > 300):
            state = "end"

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if state == "game" and event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit():
                    input_text += event.unicode
                elif event.key == pg.K_RETURN:
                    pass

            elif event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()

                if state == "start":
                    game_sfx.play()
                    game_sfx.set_volume(0.5)
                    state = "game"
                    game_start_time = current_time

                elif state == "game":
                    price = round(float(company_data["Close"].iloc[day_index]))

                    if 1000 <= x <= 1150 and 800 <= y <= 850:
                        if market_open:
                            if input_text.isdigit() and int(input_text) > 0:
                                how_much = int(input_text)
                                total_cost_of_buy = price * how_much * buy_discount
                                if money >= total_cost_of_buy:
                                    stock += how_much
                                    money -= total_cost_of_buy
                                    total_cost += price * how_much
                                    buy_sfx.play()
                                    pay_amount = int(total_cost_of_buy)
                                    frame_count = 0
                                    frame_count_2 = 0
                                    frame_count_3 = 0
                                    frame_count_4 = 0
                                    input_text = "1"
                                    start_pay_animation(True)
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
                                    sell_sfx.play( )
                                    sell_frame_count = 0
                                    sell_frame_count_2 = 0
                                    sell_frame_count_3 = 0
                                    sell_frame_count_4 = 0
                                    input_text = "1"
                                    start_pay_animation(False)
                                else:
                                    popup_info(win, "Nemáš dostatek akcií", font)
                            else:
                                popup_info(win, "Napiš prosím platné číslo", font)
                        else:
                            popup_info(win, "Dnes je zavřený trh. Nemůžeš prodávat.", font)

                elif state == "over" or state == "end":
                    state = "start"
                    money = 2000
                    stock = 0
                    profit = 0
                    rent = 0
                    total_cost = 0
                    realized_profit = 0
                    buy_discount = 1.0
                    sell_penalty = 1.0
                    market_open = True
                    input_text = "1"
                    day_index = 45
                    total_money = 0
                    game_sfx.stop()
                    company_name, company_data = random.choice(list(stocks.items()))
                    stock_price = round(float(company_data["Close"].iloc[day_index]))
                    generate_graph(company_data, day_index, company_name)
                    game_start_time = current_time

        if state == "start":
            draw_start()

        elif state == "game":
            if current_time - last_update > 0.2 and day_index < len(company_data):
                day_index += 1
                stock_price = round(float(company_data["Close"].iloc[day_index]))
                generate_graph(company_data, day_index, company_name)
                last_update = current_time

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

        elif state == "end":
            total_money = money + round(float(company_data["Close"].iloc[day_index]))
            if total_money <= 1999:
                draw_survived()
            elif 2000 <= total_money < 3999:
                draw_profit()
            elif total_money >= 4000:
                draw_rich()

        elif state == "over":
            draw_game_over()
            lose_sfx.play()

    pg.quit()
if __name__ == "__main__":
    main()
