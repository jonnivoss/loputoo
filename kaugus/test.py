import random
from enum import Enum
import math
from dataclasses import dataclass
import keyboard_maker as kb

class f(Enum):
    lp = 0
    lr = 1
    lm = 2
    li = 3
    ri = 4
    rm = 5
    rr = 6
    rp = 7
    thumb = 8


@dataclass
class key:
    x : float
    y : float
    finger : f
    offset: float = 0.0

    def __post_init__(self):
        if self.y == 0.0:
            self.offset = 0.0
        elif self.y == 1.0:
            self.offset = 0.25
        else:
            self.offset = -0.25

last_finger = f.ri

last_pos_of_fingers = {}
letter_freq = {}

def finger_distance(char1,keyboard):
    global last_finger
    char1 = char1.lower()

    if char1 == ' ':
        return 0.0

    if char1 not in keyboard:
        return 3.0

    x = 0.0
    current_char = keyboard[char1]
    for last, letter in last_pos_of_fingers.items():
        if current_char.finger.value == last.value:
            x = math.sqrt(((current_char.x + current_char.offset) - (keyboard[letter].x + keyboard[letter].offset) ) ** 2
                          + (current_char.y - keyboard[letter].y) ** 2)
            last_pos_of_fingers[last] = char1

    if last_finger.value != current_char.finger.value:
        for letters, keys in keyboard.items():
            if keys.finger.value == last_finger.value and keys.home_row:
                last_pos_of_fingers[keys.finger] = letters
        last_finger = f(current_char.finger.value)

    return x


def text_distance(text,keyboard):
    total_distance = 0.0

    with open(text, encoding='utf-8') as text_file:
        for line in text_file:
            for i in range(len(line)):
                distance = finger_distance(line[i],keyboard)
                total_distance += distance
        text_file.close()
    return total_distance



text = "text.txt"
#keyboard = kb.make_layout("kboard.txt")

def print_layout(keyboard):
    sorted_keyboard = dict(sorted(keyboard.items(), key=lambda item: (item[1].y, item[1].x)))
    i = 0
    f = open("newkey.txt", "w", encoding='utf-8')
    for letter, keys in sorted_keyboard.items():
        if keys.home_row:
            f.write(letter)
    f.write("\n")
    for letter, keys in sorted_keyboard.items():
        print(f"{letter}({int(keys.home_row)})",end=' ')
        f.write(letter)
        i += 1
        if i%12 == 0:
            print()
            f.write("\n")
    f.write("\n")
    f.close()



def find_distance(keyboard):

    #set defaiult pos to home row
    for l, k in keyboard.items():
        if k.home_row:
            last_pos_of_fingers[k.finger] = l
    #print(last_pos_of_fingers)
    distance = text_distance(text,keyboard)
    print(f"The total distance needed to write the text on  is: {distance} units.")
    return distance

def randomize_layout(keyboard_):
    keys = list(keyboard_.keys())

    key1, key2 = random.sample(keys, 2)
    keyboard_[key1], keyboard_[key2] = keyboard_[key2], keyboard_[key1]

    #key1, key2 = random.sample(keys, 2)
    #keyboard_[key1], keyboard_[key2] = keyboard_[key2], keyboard_[key1]

    return keyboard_


def find_best():
    keyboard = kb.make_layout("newkey.txt")
    best_distance = find_distance(keyboard)
    print("see on algne distants")
    num = 100
    for i in range(num):
        keyboard_ = randomize_layout(keyboard.copy())
        distance = find_distance(keyboard_)
        if distance < best_distance:
            print("siin on parem")
            best_distance = distance
            keyboard = keyboard_.copy()
    print_layout(keyboard)
find_best()
