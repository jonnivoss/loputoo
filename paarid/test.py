def separate_into_pairs(word):
    pairs = {}
    for i in range(len(word) - 1):
        parr = word[i:i + 2]
        separate = list(parr)
        sorr = sorted(separate)
        pair = ''.join(sorr)
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

def generate_matrix(data):
    # Extract all unique letters from the data
    letters = set()
    for key in data.keys():
        letters.add(key[0])
        letters.add(key[1])
    letters = sorted(list(letters))

    # Initialize the matrix with zeros
    matrix = [[0 for _ in range(len(letters))] for _ in range(len(letters))]

    # Fill the matrix with values from the data
    for key, value in data.items():
        row = letters.index(key[0])
        col = letters.index(key[1])
        matrix[row][col] += value

    return matrix, letters

def print_matrix(matrix, letters):
    max_length = len(str(max(map(max, matrix))))

    for i in range(len(matrix)):
        print(letters[i], end='\t')
        for j in range(len(matrix[i])):
            print(str(matrix[j][i]).rjust(max_length), end=' ')
        print()
    print('\t', end='')
    for letter in letters:
        print(letter.rjust(max_length), end=' ')

def print_list(matrix, letters):
    # Flatten the matrix into a list of tuples (letter1, letter2, value)
    flattened_matrix = []
    for i in range(len(matrix)):
        for j in range(i, len(matrix[i])):
            if matrix[i][j] != 0:  # Exclude empty values
                flattened_matrix.append((letters[i], letters[j], matrix[i][j]))

    # Sort the flattened matrix by value
    sorted_matrix = sorted(flattened_matrix, key=lambda x: x[2], reverse=True)

    # Find the maximum length of numbers
    max_length = len(str(sorted_matrix[-1][2]))

    # Print the sorted matrix
    for entry in sorted_matrix:
        print(entry[0], end=' ')
        print(entry[1], end=' ')
        print(str(entry[2]).rjust(max_length))


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

    matrix, letters = generate_matrix(pairs_count)
    #print_matrix(matrix, letters)
    print_list(matrix, letters)


main()
