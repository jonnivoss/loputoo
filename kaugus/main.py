import test as t
import  keyboard_maker

klaviatuurid = ["qwerty.txt",
                "dvorak.txt",
                "colemak.txt",
                "workman.txt",
                "ojoo.txt"]
def lolk():
    folder = "new"
    text = "text.txt"
    lay_name = "n"
    noi = 100
    for i in range(3):
        kb = f"{folder}/{lay_name}{i}.txt"
        files = f"{folder}/{lay_name}{i+1}.txt"
        keyboard = t.find_best(text, kb, noi)
        t.print_layout(keyboard)
        t.save_layout(keyboard, files)


def teksti_pikkus(klaviatuur):
    text = "text.txt"
    key_file = "klaviatuurid/"+klaviatuur
    print(key_file)
    kb = keyboard_maker.make_layout(key_file)
    distance = t.find_distance(text, kb)
    t.print_layout(kb)
    rounded_number = "{:.2f}".format(distance)
    print(f"{text} pikkus {rounded_number}")

for kb in klaviatuurid:
    teksti_pikkus(kb)

