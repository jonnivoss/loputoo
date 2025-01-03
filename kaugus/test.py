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

def reset_fingers(keyboard):
    for letters, keys in keyboard.items():
        if keys.finger.value == last_finger.value and keys.home_row:
            last_pos_of_fingers[keys.finger] = letters

def finger_distance(char1,keyboard):
    global last_finger
    char1 = char1.lower()

    if char1 == ' ':
        return 0.0

    #kuna ei ole otseselt kättesaadav klaviatuuril kirjutades,
    #siis lihtsalt võtta pikk tee, mis
    if char1 not in keyboard:
        reset_fingers(keyboard)
        return 0.0

    x = 0.0
    #hetkene täht
    current_char = keyboard[char1]
    for last, letter in last_pos_of_fingers.items():
        #hetkel kasutatava sõrme hetke asukoha
        if current_char.finger.value == last.value:
            #arvutab sõrme liigutamise teekonna pikkuse
            x = math.sqrt(((current_char.x + current_char.offset)
                        - (keyboard[letter].x + keyboard[letter].offset) ) ** 2
                        + (current_char.y - keyboard[letter].y) ** 2)
            #muudab hetkese sõrme asukohta hetkesele tähele
            last_pos_of_fingers[last] = char1

    #kui viimati vajutatud sõrm erineb hetke sõrmest siis muuda eelmine sõrm tagasi kodu reale
    #if last_finger.value != current_char.finger.value:
    #    reset_fingers(keyboard)
    #    last_finger = f(current_char.finger.value)

    #kui sõrm on väikene siis lisa kerge kaugus juurde, sest väikse sõrm on nõrgem/lühem
    if current_char.finger.value == f.lp.value or current_char.finger.value == f.rp.value:
        x += 0.7

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

def print_layout(keyboard):
    sorted_keyboard = dict(sorted(keyboard.items(), key=lambda item: (item[1].y, item[1].x)))

    last_y = 0
    for letter, keys in sorted_keyboard.items():
        if keys.y != last_y:
            print()
            last_y = keys.y
        print(f"{letter}({int(keys.home_row)})",end=' ')
    print()

def save_layout(keyboard, files):
    sorted_keyboard = dict(sorted(keyboard.items(), key=lambda item: (item[1].y, item[1].x)))
    last_y = 0
    f = open(files, "w", encoding='utf-8')
    for letter, keys in sorted_keyboard.items():
        if keys.home_row:
            f.write(letter)
    f.write("\n")
    for letter, keys in sorted_keyboard.items():
        if keys.y != last_y:
            last_y = keys.y
            f.write("\n")
        f.write(letter)

    f.write("\n")
    f.close()

def find_distance(text,keyboard):
    last_pos_of_fingers.clear()
    #set defaiult pos to home row
    for l, k in keyboard.items():
        if k.home_row:
            last_pos_of_fingers[k.finger] = l
    distance = text_distance(text,keyboard)
    return distance

def randomize_layout(keyboard_):
    keys = list(keyboard_.keys())
    key1, key2 = random.sample(keys, 2)
    keyboard_[key1], keyboard_[key2] = keyboard_[key2], keyboard_[key1]
    return keyboard_


def find_best(text, kbs, num):
    keyboard = kb.make_layout(kbs)
    best_distance = find_distance(text,keyboard)
    best_dist = "{:.2f}".format(best_distance)
    print(f"algne distants {best_dist}")
    for i in range(num):
        keyboard_ = randomize_layout(keyboard.copy())
        distance = find_distance(text, keyboard_)
        if distance < best_distance:
            #print(f"{i}  on  {distance}")
            best_distance = distance
            keyboard = keyboard_.copy()
    best_dist = "{:.2f}".format(best_distance)
    print(f"lopp distants {best_dist}")
    return keyboard
