from enum import Enum
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
    finger : f = f.li
    home_row: bool = False
    offset: float = 0.0

    def __post_init__(self):
        if self.y == 1.0:
            self.offset = 0.25;
        elif self.y == 0.0:
            self.offset = 0.0
        else:
            self.offset = 0.75

keyboard = {
    #left hand                                                                                                                         #right hand
    'q': key(0.0, 0.0, f.lp), 'w': key(1.0, 0.0, f.lr), 'e': key(2.0, 0.0, f.lm), 'r': key(3.0, 0.0, f.li), 't': key(4.0, 0.0, f.li),  'y': key(5.0, 0.0, f.ri), 'u': key(6.0, 0.0, f.ri), 'i': key(7.0, 0.0, f.rm), 'o': key(8.0, 0.0, f.rr), 'p': key(9.0, 0.0, f.rp), 'ü': key(10.0, 0.0, f.rp), 'õ': key(11.0, 0.0, f.rp),
    'a': key(0.0, 1.0, f.lp), 's': key(1.0, 1.0, f.lr), 'd': key(2.0, 1.0, f.lm), 'f': key(3.0, 1.0, f.li), 'g': key(4.0, 1.0, f.li),  'h': key(5.0, 1.0, f.ri), 'j': key(6.0, 1.0, f.ri), 'k': key(7.0, 1.0, f.rm), 'l': key(8.0, 1.0, f.rr), 'ö': key(9.0, 1.0, f.rp), 'ä': key(10.0, 1.0, f.rp), "'": key(11.0, 1.0, f.rp),
    '<': key(-1.0, 2.0, f.lp), 'z': key(0.0, 2.0, f.lp), 'x': key(1.0, 2.0, f.lr), 'c': key(2.0, 2.0, f.lm), 'v': key(3.0, 2.0, f.li),  'b': key(4.0, 2.0, f.li), 'n': key(5.0, 2.0, f.ri), 'm': key(6.0, 2.0, f.ri), ',': key(7.0, 2.0, f.rm), '.': key(8.0, 2.0, f.rr), '-': key(9.0, 2.0, f.rp),
    #thumbsd
    ' ': key(4.0, 1.0, f.thumb),
}

def make_layout(file):
    remapped_dict = {}
    home_row = {}
    with open(file, 'r', encoding='utf-8') as file:
        j = -1
        for line in file:
            if j == -1:
                for i in range(len(line)-1):
                    home_row[line[i]] = f(i)
            else:
                for i in range(len(line)-1):
                    if line[i] == ' ':
                        continue
                    if line[i] in home_row:
                        remapped_dict[line[i]] = key(i,j,home_row[line[i]],True)
                        home_row[line[i]] = remapped_dict[line[i]]
                    elif j == 2:
                        remapped_dict[line[i]] = key(i-1, j, f(i % 9), False)
                    else:
                        remapped_dict[line[i]] = key(i,j,f(i%9),False)
            j += 1
        #home_keys = list(home_row)
        home_value = list(home_row.values())
        #siin tuleb kuidagi näpud ära mapida
        last_home = 0

        for letters, keys in remapped_dict.items():
            for i in range(len(home_row)):
                #print(letters, keys.x+ keys.offset)

                if keys.x == home_value[i].x:
                    last_home = i

                remapped_dict[letters].finger = f(last_home)
#        remapped_dict['<'].finger = f.lp

    return remapped_dict


