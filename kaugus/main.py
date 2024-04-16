 #   keyboard = {
 #       'q': (1,0), 'w': (1,1), 'e': (1,2), 'r': (1,3), 't': (2,3), 'y': (2,4), 'u': (1,4), 'i': (1,5), 'o': (1,6), 'p': (1,7),'ü': (1,8),'õ': (2,8),
 #       'a': (0,0), 's': (0,1), 'd': (0,2), 'f': (0,3), 'g': (1,3), 'h': (1,4), 'j': (0,4), 'k': (0,5), 'l': (0,6), 'ö': (0,7),'ä': (1,8),
#        'z': (1,0), 'x': (1,1), 'c': (1,2), 'v': (1,3), 'b': (2,3), 'n': (1,4), 'm': (1,4), ',': (1,5), '.': (1,6), '-': (2,7),
#        ' ': (0,9)  # Space key
#    }

from enum import Enum
import math
from dataclasses import dataclass

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

keyboard = {
    #left hand                                                                                                                         #right hand
    'q': key(0.0, 0.0, f.lp), 'w': key(1.0, 0.0, f.lr), 'e': key(2.0, 0.0, f.lm), 'r': key(3.0, 0.0, f.li), 't': key(4.0, 0.0, f.li),  'y': key(5.0, 0.0, f.ri), 'u': key(6.0, 0.0, f.ri), 'i': key(7.0, 0.0, f.rm), 'o': key(8.0, 0.0, f.rr), 'p': key(9.0, 0.0, f.rp), 'ü': key(10.0, 0.0, f.rp), 'õ': key(11.0, 0.0, f.rp),
    'a': key(0.0, 1.0, f.lp), 's': key(1.0, 1.0, f.lr), 'd': key(2.0, 1.0, f.lm), 'f': key(3.0, 1.0, f.li), 'g': key(4.0, 1.0, f.li),  'h': key(5.0, 1.0, f.ri), 'j': key(6.0, 1.0, f.ri), 'k': key(7.0, 1.0, f.rm), 'l': key(8.0, 1.0, f.rr), 'ö': key(9.0, 1.0, f.rp), 'ä': key(10.0, 1.0, f.rp), "'": key(11.0, 1.0, f.rp),
    '<': key(0.0, 2.0, f.lp), 'z': key(1.0, 2.0, f.lp), 'x': key(2.0, 2.0, f.lr), 'c': key(3.0, 2.0, f.lm), 'v': key(4.0, 2.0, f.li),  'b': key(5.0, 2.0, f.li), 'n': key(6.0, 2.0, f.ri), 'm': key(7.0, 2.0, f.ri), ',': key(8.0, 2.0, f.rm), '.': key(9.0, 2.0, f.rr), '-': key(10.0, 2.0, f.rp),
    #thumbsd
    ' ': key(4.0, 1.0, f.thumb),
}

letter_freq = {}

def finger_distance(char1,char2):
    char1 = char1.lower()
    char2 = char2.lower()

    if char1 not in keyboard or char2 not in keyboard:
        return 4

    letter_freq[char1] = letter_freq.get(char1,0) + 1

    prev_char = keyboard[char1]
    current_char = keyboard[char2]
    if prev_char.finger == current_char.finger:
        return math.sqrt(((current_char.x + current_char.offset) - (prev_char.x + prev_char.offset)) ** 2 + (current_char.y - prev_char.y) ** 2)

    return math.sqrt((current_char.x - current_char.x) ** 2 + (current_char.y - 1.0) ** 2)


def text_distance(text):
    total_distance = 0
    with open(text, encoding='utf-8') as text_file:
        for line in text_file:
            for i in range(len(line) - 1):
                distance = finger_distance(line[i], line[i + 1])
                total_distance += distance
        text_file.close()
    return total_distance


if __name__ == "__main__":
    text = "test.txt"
    distance = text_distance(text)
    print(f"The total distance needed to write the text is: {distance} units.")

    for keys in keyboard.items():
        print(f"Letter {keys}")
