def separate_into_pairs(word):
    pairs = {}
    for i in range(len(word) - 1):
        pair = word[i:i + 2]
        if pair in pairs:
            pairs[pair] += 1
        else:
            pairs[pair] = 1
    return pairs


def count_pairs_from_multiple_words(words_with_count):
    all_pairs = {}
    for word, counts in words_with_count.items():
        pairs = separate_into_pairs(word)
        for pair, pair_count in pairs.items():
            if pair in all_pairs:
                all_pairs[pair] += pair_count * counts['kokku']
            else:
                all_pairs[pair] = pair_count * counts['kokku']
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

    pairs_count = count_pairs_from_multiple_words(words_with_count)
    for pair, count in pairs_count.items():
        print(f"{count} * {pair}")


if __name__ == "__main__":
    main()
