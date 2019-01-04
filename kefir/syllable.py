
def syllable(word):
    boundaries = get_syllable_boundaries(word)
    result = []
    for i in range(0,len(boundaries)-1):
        result.append(word[boundaries[i]:boundaries[i+1]])
    if len(boundaries) > 0:
        result.append(word[boundaries[len(boundaries)-1]:])

    return result

def get_syllable_boundaries(word):
    size = len(word)
    boundary_indexes = []
    last_index = size
    index = 0
    while last_index > 0:
        letter_count = letter_count_for_last_syllable(word,last_index)
        if letter_count == -1:
            return [0]

        boundary_indexes.append(last_index - letter_count)
        index += 1
        last_index -= letter_count
    result = []
    for i in range(0,index):
        result.append(boundary_indexes[index - i - 1])
    return result

def is_vowel(character):
    if character in "aeiıoöuü":
        return True
    return False

def letter_count_for_last_syllable(chrs,end_index):
    if end_index == 0:
        return -1
    
    if is_vowel(chrs[end_index - 1]):
        if end_index == 1:
            return 1
        if is_vowel(chrs[end_index - 2]):
            return 1
        if end_index == 2:
            return 2
        if not is_vowel(chrs[end_index - 3]) and end_index == 3:
            return 3
        return 2
    else :
        if end_index == 1:
            return -1
        if is_vowel(chrs[end_index - 2]):
            if end_index == 2 or is_vowel(chrs[end_index - 3]):
                return 2
            if end_index == 3 or is_vowel(chrs[end_index - 4]):
                return 3
            if end_index == 4:
                return -1
            if not is_vowel(chrs[end_index - 5]):
                return 3
            return 3
        else:
            if not is_vowel(chrs[end_index - 2]):
                return -1
            if end_index == 2 or not is_vowel(chrs[end_index - 2]):
                return -1
            if end_index > 3 and not is_vowel(chrs[end_index - 4]):
                return 4
            return 3

