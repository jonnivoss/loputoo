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
    return sorted_matrix


def something(data):
    letters = set()
    for key in data.keys():
        letters.add(key[0])
        letters.add(key[1])
    letters = sorted(list(letters))
    print(letters)
    singel_list = {}
    for key, value in data.items():
        if key[0] in singel_list:
            singel_list[key[0]] += value
        else:
            singel_list[key[0]] = value

        if key[1] in singel_list:
            singel_list[key[1]] += value
        else:
            singel_list[key[1]] = value
    sorted_dic = sorted(singel_list.items(),key=lambda  x: x[1],reverse=True)
    return sorted_dic

def single_letter_count(wwc):
    all_pairs = {}
    total_count = 0
    for word, counts in wwc.items():
        for letter in word.lower():
            if letter == '-':
                continue
            total_count += counts['kokku']
            if letter in all_pairs:
                all_pairs[letter] += counts['kokku']
            else:
                all_pairs[letter] = counts['kokku']
    sorted_by_letter = sorted(all_pairs.items(), key=lambda item: item[1], reverse=True)
    #sorted_by_letter = sorted(all_pairs.items())
    print(total_count,sorted_by_letter)
    for letter, count in sorted_by_letter:
        rounded_number = round(count/total_count, 5) * 100
        print(f"{letter} - {rounded_number:.5f}%")



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

    single_letter_count(words_with_count)
    #pairs_count = count_pairs_from_multiple_words(words_with_count)
    #single_letter_count = something(pairs_count)
    #print(single_letter_count)
    #matrix, letters = generate_matrix(pairs_count)
    #print_matrix(matrix, letters)
    #list_pair = print_list(matrix, letters)
    #print(list_pair)


main()
