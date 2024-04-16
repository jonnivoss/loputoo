 #   keyboard = {
 #       'q': (1,0), 'w': (1,1), 'e': (1,2), 'r': (1,3), 't': (2,3), 'y': (2,4), 'u': (1,4), 'i': (1,5), 'o': (1,6), 'p': (1,7),'ü': (1,8),'õ': (2,8),
 #       'a': (0,0), 's': (0,1), 'd': (0,2), 'f': (0,3), 'g': (1,3), 'h': (1,4), 'j': (0,4), 'k': (0,5), 'l': (0,6), 'ö': (0,7),'ä': (1,8),
#        'z': (1,0), 'x': (1,1), 'c': (1,2), 'v': (1,3), 'b': (2,3), 'n': (1,4), 'm': (1,4), ',': (1,5), '.': (1,6), '-': (2,7),
#        ' ': (0,9)  # Space key
#    }

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
            self.offset = 0.0;
        elif self.y == 1.0:
            self.offset = 0.25
        else:
            self.offset = -0.25

last_finger = f.ri
keyboard = {}
last_pos_of_fingers = {}
letter_freq = {}

def finger_distance(char1):
    global last_finger
    char1 = char1.lower()

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


def text_distance(text):
    total_distance = 0.0

    with open(text, encoding='utf-8') as text_file:
        for line in text_file:
            for i in range(len(line)):
                distance = finger_distance(line[i])
                total_distance += distance
        text_file.close()
    return total_distance



text = "text.txt"
keyboard = kb.make_layout("kboard.txt")

#set defaiult pos to home row
for l, k in keyboard.items():
    if k.home_row:
        last_pos_of_fingers[k.finger] = l

distance = text_distance(text)
print(f"The total distance needed to write the text is: {distance} units.")

for letter, keys in keyboard.items():
    print(f"{letter}",end=' ')
