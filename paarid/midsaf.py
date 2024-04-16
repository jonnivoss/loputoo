def separate_into_letters(word):
    letters = {}
    for i in range(len(word)):
        letter = word[i]
        if letter in letters:
            letters[letter] += 1
        else:
            letters[letter] = 1
    return letters


def count_letters(words_with_count):
    all_pairs = {}
    for word, counts in words_with_count.items():
        letters = separate_into_letters(word)
        for letter, letter_count in letters.items():
            if letter in all_pairs:
                all_pairs[letter] += letter_count * counts['kokku']
            else:
                all_pairs[letter] = letter_count * counts['kokku']
    return all_pairs


def main():
    file_name = "tabel1.txt"
    words_with_count = {}
    with open(file_name, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            parts = line.strip().split('\t')
            word = parts[0]
            counts = {'kokku': int(parts[2])}
            words_with_count[word] = counts

    pairs_count = count_letters(words_with_count)

    #sorted_matrix = sorted(pairs_count, reverse=True)

    for pair, count in pairs_count.items():
        print(f"{count} : {pair}")

main()