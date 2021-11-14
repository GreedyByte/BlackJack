import random
import tkinter
import pygame
from tkinter import *
from PIL import Image, ImageTk

global root
global player_frame
global player_sum_frame
global reply_frame
global player_sum_text
global player_sum_label
global dealer_frame
global dealer_sum_frame
global dealer_sum_text
global dealer_sum_label
global lose_label
global blackjack_label
global shown_card_label
global win_label
global draw_label
global bust_label
global hit_button
global stand_button
global hidden_card_render
global hidden_card_value
global hidden_card_label
global cards_render
global cards_image
global back_card
global back_card_label
global buttons_frame
global split_button

global left_hit_button
global left_stand_button
global left_cards_frame
global right_cards_frame
global left_sum_text
global right_sum_text
global left_reply_frame
global right_reply_frame
global right_stand_button
global right_hit_button
global bottom_frame
global chips_image
global chips_render

cards_num = []
player_used_cards_img = []
cards = []
for x in range(1, 14):
    for y in range(0, 4):
        if x > 10:
            cards.append(10)  # create card value list (face cards value = 10)
        else:
            cards.append(x)

need_shuffle = False
cards_remaining = 52
player_hand = []  # value of cards 0-10 (face cards = 10)
player_right_hand = []
player_left_hand = []
player_cards = []  # number of cards 0-13
dealer_hand = []
player_right_sum = 0
player_left_sum = 0
player_sum = 0
dealer_sum = 0
money = 1000
betted_amount = 0
bg_color = '#076324'
after_game_wait = 2000


def wait_here(time):
    var = IntVar()
    root.after(time, var.set, 1)
    root.wait_variable(var)


def card_anim(frame, input_side):  # prints back_card for <time> sec animation
    back_card_temp = Label(frame, image=back_card, bg=bg_color)
    back_card_temp.image = back_card_temp
    back_card_temp.pack(side=input_side)
    wait_here(350)
    back_card_temp.destroy()
    pygame.mixer.music.load("sound/flip1.mp3")  # Loading File Into Mixer
    pygame.mixer.music.play()  # Playing It In The Whole Device


def draw_card(times, show, location, hand):  # draw card times, show the card or not, player or dealer side
    i = 0
    global cards_remaining
    global player_hand
    global dealer_hand
    global need_shuffle

    if cards_remaining < 20:
        need_shuffle = True
    if times > cards_remaining:
        print('Not Enough Cards')
        return
    else:
        cards_remaining -= times  # tells how many cards remain
        # print(cards_remaining)  # error after game when print
    if show is False and times > 1:
        print('Cant draw more than one "hidden" card')
        return

    while i < times:

        num = random.randint(0, cards_remaining)

        if show:
            hand.append(cards[num])  # append the card in hand(as argument)
            if location != dealer_frame:
                player_used_cards_img.append(cards_render[num])

            card_anim(location, LEFT)  # animation

            card_label = Label(location, image=cards_render[num], bg=bg_color)
            card_label.image = cards_render[num]
            card_label.pack(side=LEFT)

        else:
            global hidden_card_render
            global hidden_card_value
            global back_card_label

            hidden_card_render = cards_render[num]  # get img of hidden card to show later
            hidden_card_value = cards[num]  # get value of card to use later

            back_card_label = Label(dealer_frame, image=back_card, bg=bg_color)
            back_card_label.image = back_card_label
            back_card_label.pack(side=LEFT)  # above code to show hidden card

            del cards[num]  # delete card value
            del cards_render[num]  # delete cards_renderer
            return

        del cards[num]  # delete card value
        del cards_render[num]  # delete img_card
        i += 1


def update_sum(target_text, hand, hidden_card_add):
    global player_sum
    global dealer_sum
    global player_left_sum
    global player_right_sum

    sum_11 = 0  # player sum if aces are value 11
    sum_1 = 0  # player sum if aces are value 1
    no_aces = True

    for card in hand:  # get sum if only the first ace is value 11 (2 cards MAX value 21)
        if card == 1 and no_aces is True:
            sum_11 += 11
            no_aces = False
        else:
            sum_11 += card

    for card in hand:
        sum_1 += card

    if hidden_card_add:  # add hidden_card value in sum (also modifies it if its an ace)
        if hidden_card_value == 1:
            sum_11 += 11
        else:
            sum_11 += hidden_card_value

        sum_1 += hidden_card_value

    temp_sum = 0
    if sum_11 > 21:
        target_text.set(sum_1)  # print sum_1
        temp_sum = sum_1
    elif sum_11 < 21 and no_aces:
        target_text.set(sum_11)  # print sum_1 or sum_11 same shit
        temp_sum = sum_11
    elif sum_11 < 21:
        target_text.set(f'{sum_1} / {sum_11}')  # print sum_1 and sum_11
        temp_sum = sum_11
    elif sum_11 == 21:
        target_text.set(sum_11)  # print sum_11
        temp_sum = sum_11

    if target_text == dealer_sum_text:
        dealer_sum = temp_sum
    elif target_text == player_sum_text:
        player_sum = temp_sum
    elif target_text == left_sum_text:
        player_left_sum = temp_sum
    elif target_text == right_sum_text:
        player_right_sum = temp_sum
    else:
        print('error sum not updated')


def new_deck():
    global cards_remaining
    global cards
    global need_shuffle

    need_shuffle = False
    cards_remaining = 52

    cards.clear()
    for x in range(1, 14):
        for y in range(0, 4):
            if x > 10:
                cards.append(10)
            else:
                cards.append(x)

    cards_render.clear()
    for x in range(0, 52):
        cards_render.append(ImageTk.PhotoImage(cards_image[x]))


def game_start():
    global stand_button
    global hit_button
    global cards_remaining

    if need_shuffle:  # check if its time to shuffle cards
        new_deck()

    draw_card(2, True, player_frame, player_hand)  # get sum and print cards

    draw_card(1, True, dealer_frame, dealer_hand)  # get sum and print the shown card
    draw_card(1, False, dealer_frame, dealer_hand)  # print the hidden card

    update_sum(player_sum_text, player_hand, False)  # update values on screen and sums
    update_sum(dealer_sum_text, dealer_hand, False)

    hit_button.grid(row=0, column=2, padx=2)

    stand_button.grid(row=0, column=0, padx=2)

    if hidden_card_value == 1:  # if hidden card is ace set value to 11
        temp_add_value = 11
    else:
        temp_add_value = hidden_card_value

    # dealer sum here doesnt have the value of hidden_card so we add it
    if dealer_sum + temp_add_value == 21 and player_sum == 21:  # dealer_sum (shown card) temp_. (hidden card)
        flip_hidden_card()
        update_sum(dealer_sum_text, dealer_hand, True)

        hit_button['state'] = DISABLED
        stand_button['state'] = DISABLED
        print_draw(reply_frame)

        wait_here(after_game_wait)
        restart_game()

    elif dealer_sum + temp_add_value == 21:
        flip_hidden_card()
        update_sum(dealer_sum_text, dealer_hand, True)

        hit_button['state'] = DISABLED
        stand_button['state'] = DISABLED

        blackjack_label.config(text='Dealer Hit BlackJack')
        blackjack_label.pack(side=BOTTOM)
        print_lose(reply_frame)

        wait_here(after_game_wait)
        restart_game()

    elif player_sum == 21:
        hit_button['state'] = DISABLED
        stand_button['state'] = DISABLED

        print_blackjack(reply_frame)

        wait_here(after_game_wait)
        restart_game()

    if player_hand[0] == player_hand[1] and money >= betted_amount:
        split_button.grid(row=0, column=1, padx=2)

def get_bet():
    global chips_frame
    global text_frame
    chips_frame = Frame(bottom_frame, bg=bg_color, pady=10)
    chips_frame.pack(side=BOTTOM)
    text_frame = Frame(bottom_frame, bg=bg_color)
    text_frame.pack(side=TOP)
    bet_buttons_frame = Frame(text_frame)
    bet_buttons_frame.grid(row=3, column=0)

    thrown_chips_frame = Frame(text_frame, bg=bg_color)
    thrown_chips_frame.grid(row=0, column=0)

    for x in range(0,3):
        randx = random.randint(0, 100)
        randy = random.randint(0, 100)
        random_chip = Label(thrown_chips_frame, image=chips_render[x], bg=bg_color)
        random_chip.place(height=100, width=100, relx=randx, rely=randy)


    chips_buttons = {}
    for x in range(0, 9):

        def func(i=x):
            return chips_math(i)

        chips_buttons[x] = (Button(chips_frame, image=chips_render[x],
                                    command=func, bg=bg_color, border=0,
                                    activebackground=bg_color))
        chips_buttons[x].pack(side=LEFT)

    global money_text
    global thrown_money_text
    global place_bet_button

    thrown_money_text = tkinter.StringVar()
    money_text = tkinter.StringVar()
    money_text.set(f'Money : {money} $')

    money_text_label = Label(text_frame, textvariable=money_text, bg=bg_color, font=('Arial', 15), pady=20)
    money_text_label.grid(row=4, column=0)

    place_bet_button = Button(bet_buttons_frame, text='Place Bet', command=bet_placed, font=('Arial', 15))
    place_bet_button.pack(side=LEFT)
    place_bet_button['state'] = DISABLED

    reset_bet_button = Button(bet_buttons_frame, text='Reset Bet', command=reset_bet, font=('Arial', 15))
    reset_bet_button.pack(side=LEFT)


    thrown_money_label = Label(text_frame, textvariable=thrown_money_text, bg=bg_color, font=('Arial', 15), pady=20)
    thrown_money_label.grid(row=2, column=0)

    select_text_label = Label(text_frame, text='Select Bet', bg=bg_color,font=('Arial', 25))
    select_text_label.grid(row=1, column=0)


def reset_bet():
    global money
    global betted_amount

    money += betted_amount
    betted_amount = 0

    place_bet_button['state']=DISABLED

    money_text.set(f'Money : {money} $')
    thrown_money_text.set(f'Bet = {betted_amount} $')

def chips_math(index):
    global money
    global betted_amount

    amount = 0

    if index == 0:
        amount = 1
    elif index == 1:
        amount = 5
    elif index == 2:
        amount = 10
    elif index == 3:
        amount = 25
    elif index == 4:
        amount = 50
    elif index == 5:
        amount = 100
    elif index == 6:
        amount = 250
    elif index == 7:
        amount = 500
    elif index == 8:
        amount = 1000

    if money < amount:
        money_text.set('Not enough Money')
        wait_here(1000)
        money_text.set(f'Money : {money} $')
    else:
        place_bet_button['state'] = ACTIVE
        money -= amount
        betted_amount += amount
        money_text.set(f'Money : {money} $')
        thrown_money_text.set(f'Bet = {betted_amount} $')

def bet_placed():
    text_frame.destroy()
    chips_frame.destroy()
    game_start()

def split():
    global left_hit_button
    global left_stand_button
    global left_cards_frame
    global right_cards_frame
    global left_sum_text
    global right_sum_text
    global left_reply_frame
    global right_reply_frame
    global right_stand_button
    global right_hit_button
    global bottom_frame
    global money

    money -= betted_amount  # betting in two hands so we bet the same amount again

    # clean GUI
    player_frame.destroy()
    player_sum_frame.destroy()
    buttons_frame.destroy()
    # create GUI
    player_left_hand.append(player_hand[0])
    player_right_hand.append(player_hand[1])

    bottom_frame = Frame(root, bg=bg_color)
    bottom_frame.pack(side=BOTTOM)

    left_sum_text = tkinter.StringVar()
    right_sum_text = tkinter.StringVar()

    left_reply_frame = Frame(bottom_frame, bg=bg_color, padx=100)
    left_reply_frame.grid(row=0, column=0)

    right_reply_frame = Frame(bottom_frame, bg=bg_color, padx=100)
    right_reply_frame.grid(row=0, column=1)

    left_buttons_frame = Frame(bottom_frame, bg=bg_color, padx=100)
    left_buttons_frame.grid(row=1, column=0)

    right_buttons_frame = Frame(bottom_frame, bg=bg_color, padx=100)
    right_buttons_frame.grid(row=1, column=1)

    left_sum_frame = Frame(bottom_frame, bg=bg_color, padx=100)
    left_sum_frame.grid(row=2, column=0)

    right_sum_frame = Frame(bottom_frame, bg=bg_color, padx=100)
    right_sum_frame.grid(row=2, column=1)

    left_cards_frame = Frame(bottom_frame, bg=bg_color, padx=100)
    left_cards_frame.grid(row=3, column=0)

    right_cards_frame = Frame(bottom_frame, bg=bg_color, padx=100)
    right_cards_frame.grid(row=3, column=1)

    left_card = Label(left_cards_frame, image=player_used_cards_img[0], bg=bg_color)
    left_card.image = player_used_cards_img[0]
    left_card.pack(side=LEFT)

    right_card = Label(right_cards_frame, image=player_used_cards_img[1], bg=bg_color)
    right_card.image = player_used_cards_img[1]
    right_card.pack(side=LEFT)

    left_sum_label = Label(left_sum_frame, textvariable=left_sum_text, font=('', 15), bg=bg_color)
    right_sum_label = Label(right_sum_frame, textvariable=right_sum_text, font=('', 15), bg=bg_color)
    left_sum_label.pack()
    right_sum_label.pack()

    left_hit_button = Button(left_buttons_frame, text='Hit', command=left_hand_hit,
                             width=6, pady=3, activebackground='#11A612',
                             font='Trebuchet')

    left_stand_button = Button(left_buttons_frame, text='Stand', command=left_hand_stand,
                               width=6, pady=3, activebackground='#FF2600',
                               font='Trebuchet')

    right_hit_button = Button(right_buttons_frame, text='Hit', command=right_hand_hit,
                              width=6, pady=3, activebackground='#11A612',
                              font='Trebuchet')

    right_stand_button = Button(right_buttons_frame, text='Stand', command=right_hand_stand,
                                width=6, pady=3, activebackground='#FF2600',
                                font='Trebuchet')

    left_stand_button.pack(side=LEFT)
    left_hit_button.pack(side=LEFT)

    # draw a secondary card Left
    draw_card(1, True, left_cards_frame, player_left_hand)

    update_sum(left_sum_text, player_left_hand, False)

    if player_left_sum == 21:
        left_hand_stand()


def left_hand_stand():
    left_hit_button['state'] = DISABLED
    left_stand_button['state'] = DISABLED

    draw_card(1, True, right_cards_frame, player_right_hand)
    update_sum(right_sum_text, player_right_hand, False)

    if player_right_sum == 21:
        right_hand_stand()

    right_stand_button.pack(side=LEFT)
    right_hit_button.pack(side=LEFT)


def left_hand_hit():
    left_hit_button['state'] = DISABLED
    left_stand_button['state'] = DISABLED

    draw_card(1, True, left_cards_frame, player_left_hand)
    update_sum(left_sum_text, player_left_hand, False)

    left_hit_button['state'] = ACTIVE
    left_stand_button['state'] = ACTIVE

    if player_left_sum > 21:

        left_hit_button['state'] = DISABLED  # hit after lose fix
        left_stand_button['state'] = DISABLED  # stand after lose fix

        left_hand_stand()
    elif player_left_sum == 21:
        left_hand_stand()


def right_hand_hit():
    right_hit_button['state'] = DISABLED
    right_stand_button['state'] = DISABLED

    draw_card(1, True, right_cards_frame, player_right_hand)
    update_sum(right_sum_text, player_right_hand, False)

    right_hit_button['state'] = ACTIVE
    right_stand_button['state'] = ACTIVE

    if player_right_sum > 21:

        right_hit_button['state'] = DISABLED  # hit after lose fix
        right_stand_button['state'] = DISABLED  # stand after lose fix
        right_hand_stand()
    elif player_right_sum == 21:
        right_hand_stand()


def right_hand_stand():
    right_stand_button['state'] = DISABLED
    right_hit_button['state'] = DISABLED

    update_sum(dealer_sum_text, dealer_hand, True)
    update_sum(left_sum_text, player_left_hand, False)
    update_sum(right_sum_text, player_right_hand, False)

    flip_hidden_card()

    while dealer_sum < 17:
        draw_card(1, True, dealer_frame, dealer_hand)
        update_sum(dealer_sum_text, dealer_hand, True)


    if player_left_sum > 21:
        print_bust(left_reply_frame)
    elif dealer_sum > 21:
        print_win(left_reply_frame)
    elif player_left_sum > dealer_sum:
        print_win(left_reply_frame)
    elif player_left_sum < dealer_sum:
        print_lose(left_reply_frame)
    elif player_left_sum == dealer_sum:
        print_draw(left_reply_frame)

    if player_right_sum > 21:
        print_bust(right_reply_frame)
    elif dealer_sum > 21:
        print_win(right_reply_frame)
    elif player_right_sum > dealer_sum:
        print_win(right_reply_frame)
    elif player_right_sum < dealer_sum:
        print_lose(right_reply_frame)
    elif player_right_sum == dealer_sum:
        print_draw(right_reply_frame)

    wait_here(after_game_wait)
    restart_game()

def print_blackjack(location):
    global money
    blackjack_label1 = Label(location, text=f'BLACKJACK\nYou Won {betted_amount * 2.5} $')
    blackjack_label1.config(font=('', 30), bg=bg_color)
    blackjack_label1.pack()

    money += betted_amount * 2.5

def print_win(location):
    global money
    win_label1 = Label(location, text=f'You Won {betted_amount * 2} $')
    win_label1.config(font=('', 30), bg=bg_color)
    win_label1.pack(side=BOTTOM)

    money += betted_amount * 2


def print_lose(location):
    win_label1 = Label(location, text='YOU LOSE')
    win_label1.config(font=('', 30), bg=bg_color)
    win_label1.pack(side=BOTTOM)


def print_draw(location):
    global money

    money += betted_amount

    draw_label1 = Label(location, text='DRAW')
    draw_label1.config(font=('', 30), bg=bg_color)
    draw_label1.pack(side=BOTTOM)


def print_bust(location):
    bust_label1 = Label(location, text='BUST')
    bust_label1.config(font=('', 30), bg=bg_color)
    bust_label1.pack(side=BOTTOM)

def flip_hidden_card():
    back_card_label.destroy()
    pygame.mixer.music.load("sound/flip1.mp3")  # Loading File Into Mixer
    pygame.mixer.music.play()  # Playing It In The Whole Device
    shown_card_label = Label(dealer_frame, image=hidden_card_render, bg=bg_color)
    shown_card_label.image = hidden_card_render
    shown_card_label.pack(side=LEFT)

def stand():
    global shown_card_label

    hit_button['state'] = DISABLED
    stand_button['state'] = DISABLED
    split_button['state'] = DISABLED

    update_sum(dealer_sum_text, dealer_hand, True)
    update_sum(player_sum_text, player_hand, False)

    flip_hidden_card()

    while True:  # game logic
        if dealer_sum > 21:
            print_win(reply_frame)
            break
        elif dealer_sum < 17:
            draw_card(1, True, dealer_frame, dealer_hand)
            update_sum(dealer_sum_text, dealer_hand, True)
        elif dealer_sum > player_sum:
            print_lose(reply_frame)
            break
        elif dealer_sum < player_sum:
            print_win(reply_frame)
            break
        elif dealer_sum == player_sum:
            print_draw(reply_frame)
            break
        else:
            print('error')

    wait_here(after_game_wait)
    restart_game()


def hit():
    hit_button['state'] = DISABLED  # multiple hit calls fix
    stand_button['state'] = DISABLED
    split_button['state'] = DISABLED

    draw_card(1, True, player_frame, player_hand)
    update_sum(player_sum_text, player_hand, False)

    stand_button['state'] = ACTIVE
    hit_button['state'] = ACTIVE  # multiple hit calls fix

    if player_sum > 21:

        hit_button['state'] = DISABLED  # hit after lose fix
        stand_button['state'] = DISABLED  # stand after lose fix

        print_bust(reply_frame)
        wait_here(after_game_wait)
        restart_game()
    elif player_sum == 21:
        stand()


class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        self.is_true = True
        self.master.geometry('1200x700')
        master.attributes('-fullscreen', True)
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        if self.is_true is True:
            self.master.attributes('-fullscreen', False)
            self.is_true = False
        else:
            self.master.attributes('-fullscreen', True)
            self.is_true = True


def gui_start(restart):
    global root
    global player_frame
    global player_sum_frame
    global reply_frame
    global buttons_frame
    global player_sum_text
    global player_sum_label
    global dealer_frame
    global dealer_sum_frame
    global dealer_sum_text
    global dealer_sum_label
    global lose_label
    global blackjack_label
    global shown_card_label
    global win_label
    global draw_label
    global bust_label
    global hit_button
    global stand_button
    global split_button
    global bottom_frame

    if restart is False:
        root = Tk()
        pygame.init()

        global cards_render
        global cards_image
        global chips_image
        global chips_render
        global back_card

        cards_image = []
        cards_render = []
        for x in range(0, 52):
            cards_image.append(Image.open(f"images/cards/cards({x + 1}).png"))
            cards_image[x] = cards_image[x].resize((100, 150))
            cards_render.append(ImageTk.PhotoImage(cards_image[x]))

        chips_image = []
        chips_render = []
        for x in range(0, 9):
            chips_image.append(Image.open(f'images/chips/{x+1}.png'))
            chips_image[x] = chips_image[x].resize((100, 100))
            chips_render.append(ImageTk.PhotoImage(chips_image[x]))

        back_card_open = Image.open('images/cards/back_card.png')
        back_card_open = back_card_open.resize((100, 150))
        back_card = ImageTk.PhotoImage(back_card_open)

        root.title('BlackJack')
        root.config(bg=bg_color)
        FullScreenApp(root)

    bottom_frame = Frame(root, bg=bg_color)
    bottom_frame.pack(side=BOTTOM)

    player_frame = Frame(bottom_frame)
    player_frame.config(bg=bg_color)
    player_frame.pack(side=BOTTOM)

    player_sum_frame = Frame(bottom_frame)
    player_sum_frame.config(bg=bg_color)
    player_sum_frame.pack(side=BOTTOM)

    buttons_frame = Frame(bottom_frame)
    buttons_frame.config(bg=bg_color)
    buttons_frame.pack(side=BOTTOM)

    reply_frame = Frame(bottom_frame)
    reply_frame.config(bg=bg_color)
    reply_frame.pack(side=BOTTOM)

    player_sum_text = tkinter.StringVar()
    player_sum_label = Label(player_sum_frame, textvariable=player_sum_text)
    player_sum_label.config(font=('', 15), bg=bg_color)
    player_sum_label.pack(side=BOTTOM)

    dealer_frame = Frame(root)
    dealer_frame.config(bg=bg_color)
    dealer_frame.pack(side=TOP)
    dealer_sum_frame = Frame(root)
    dealer_sum_frame.config(bg=bg_color)
    dealer_sum_frame.pack(side=TOP)

    dealer_sum_text = tkinter.StringVar()
    dealer_sum_label = Label(dealer_sum_frame, textvariable=dealer_sum_text)
    dealer_sum_label.config(font=('', 15), bg=bg_color)
    dealer_sum_label.pack(side=TOP)

    bust_label = Label(reply_frame, text='BUST')
    bust_label.config(font=('', 30), bg=bg_color)

    blackjack_label = Label(reply_frame, text='BLACKJACK')
    blackjack_label.config(font=('', 30), bg=bg_color)

    win_label = Label(reply_frame, text='YOU WON')
    win_label.config(font=('', 30), bg=bg_color)

    lose_label = Label(reply_frame, text='YOU LOST')
    lose_label.config(font=('', 30), bg=bg_color)

    draw_label = Label(reply_frame, text='DRAW')
    draw_label.config(font=('', 30), bg=bg_color)

    hit_button = Button(buttons_frame, text='Hit', command=hit,
                        width=6, pady=3, activebackground='#11A612',
                        font='Trebuchet')

    stand_button = Button(buttons_frame, text='Stand', command=stand,
                          width=6, pady=3, activebackground='#FF2600',
                          font='Trebuchet')

    split_button = Button(buttons_frame, text='Split', command=split, width=6, pady=3, font='Trebuchet')

    get_bet()

    root.mainloop()


def restart_game():
    global player_sum
    global dealer_sum
    global player_hand
    global dealer_hand
    global player_right_sum
    global player_left_sum
    global betted_amount

    player_used_cards_img.clear()
    player_hand.clear()
    player_right_hand.clear()
    player_left_hand.clear()
    player_cards.clear()
    dealer_hand.clear()

    player_left_sum = 0
    player_right_sum = 0
    player_sum = 0
    dealer_sum = 0
    betted_amount = 0

    bottom_frame.destroy()
    dealer_frame.destroy()
    dealer_sum_frame.destroy()

    gui_start(True)


gui_start(False)
