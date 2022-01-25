import difflib
import re
import pandas as pd
import xlrd
import csv
from fuzzywuzzy import fuzz
from wsong_typo_distance import typoDistance


# wsong_typo_distance uses an edited version of: https://github.com/wsong/Typo-Distance/blob/master/typodistance.py
# the edit adjusts for a British QWERTY keyboard.
# Adjusted version can be found here: https://github.com/GrinningTrickster/Typo-Distance
# fuzzywuzzy is from: https://github.com/seatgeek/fuzzywuzzy
# pandas is from: https://pandas.pydata.org/

# To find the difference in word lengths between the original word and the variant.
def word_length_difference(original, variant):
    original_length = len(original)
    variant_length = len(variant)
    difference = original_length - variant_length
    return difference


# Identify whether there is a full, partial or no match between the first and last letters of the original name
# versus the variant.
def first_last_letter_match(original, variant):
    original_word_length = len(original) - 1
    variant_word_length = len(variant) - 1
    original_first = original[0]
    original_last = original[original_word_length]
    variant_first = variant[0]
    variant_last = variant[variant_word_length]
    result = 0
    # full match
    if original_first == variant_first and original_last == variant_last:
        result = 3
    # first letter match
    elif original_first == variant_first and original_last != variant_last:
        result = 1
    # last letter match
    elif original_first != variant_first and original_last == variant_last:
        result = 2
    # no match
    else:
        result = 0
    return result


# Regardless of whether characters are added to the beginning or the end of the variant, does the variant contain the
# original name?
def original_name_match(original, variant):
    match = re.match(".*" + original + ".*", variant)
    result = "Error"
    if match is None:
        result = 0
    else:
        result = 1
    return result


# Custom-built function to quantify the similarity between the original and variant based on the position of
# characters on a British QWERTY keyboard. The idea is that not all variations are built on visual similarities, but
# also on keyboard distance (where people are likely to make typos).
def distance_difference(name):
    keyboard_distance = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "0": 10,
        "_": 11,
        "q": 1,
        "w": 2,
        "e": 3,
        "r": 4,
        "t": 5,
        "y": 6,
        "u": 7,
        "i": 8,
        "o": 9,
        "p": 10,
        "a": 1,
        "s": 2,
        "d": 3,
        "f": 4,
        "g": 5,
        "h": 6,
        "j": 7,
        "k": 8,
        "l": 9,
        "z": 1,
        "x": 2,
        "c": 3,
        "v": 4,
        "b": 5,
        "n": 6,
        "m": 7

    }

    keyboard_line_numbers = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "0": 10,
        "_": 11
    }

    keyboard_line_one = {
        "q": 1,
        "w": 2,
        "e": 3,
        "r": 4,
        "t": 5,
        "y": 6,
        "u": 7,
        "i": 8,
        "o": 9,
        "p": 10
    }

    keyboard_line_two = {
        "a": 1,
        "s": 2,
        "d": 3,
        "f": 4,
        "g": 5,
        "h": 6,
        "j": 7,
        "k": 8,
        "l": 9
    }

    keyboard_line_three = {
        "z": 1,
        "x": 2,
        "c": 3,
        "v": 4,
        "b": 5,
        "n": 6,
        "m": 7
    }

    final_distance = 0
    next_letter = 0
    for letter in name:
        if next_letter < len(name) - 1:
            next_letter = next_letter + 1
            next_character = name[next_letter]
            distance = keyboard_distance[letter] - \
                       keyboard_distance[next_character]
            if next_character in keyboard_line_numbers \
                    and letter in keyboard_line_numbers \
                    or next_character in keyboard_line_one \
                    and letter in keyboard_line_one \
                    or next_character in keyboard_line_two \
                    and letter in keyboard_line_two \
                    or next_character in keyboard_line_three \
                    and letter in keyboard_line_three:
                final_distance = final_distance + abs(distance)
            elif next_character in keyboard_line_numbers \
                    and letter in keyboard_line_one \
                    or next_character in keyboard_line_one \
                    and letter in keyboard_line_two \
                    or next_character in keyboard_line_two \
                    and letter in keyboard_line_three \
                    or next_character in keyboard_line_one \
                    and letter in keyboard_line_numbers \
                    or next_character in keyboard_line_two \
                    and letter in keyboard_line_one \
                    or next_character in keyboard_line_three \
                    and letter in keyboard_line_two:
                final_distance = final_distance + abs(distance) + 1
            elif next_character in keyboard_line_numbers \
                    and letter in keyboard_line_three \
                    or next_character in keyboard_line_three \
                    and letter in keyboard_line_numbers:
                final_distance = final_distance + abs(distance) + 3
            else:
                final_distance = final_distance + abs(distance) + 2
    # print(name + " " + str(final_distance))
    return final_distance

# for keyboard distance weighting
def letter_addition(variant):
    keyboard_distance = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "0": 10,
        "_": 11,
        "q": 1,
        "w": 2,
        "e": 3,
        "r": 4,
        "t": 5,
        "y": 6,
        "u": 7,
        "i": 8,
        "o": 9,
        "p": 10,
        "a": 1,
        "s": 2,
        "d": 3,
        "f": 4,
        "g": 5,
        "h": 6,
        "j": 7,
        "k": 8,
        "l": 9,
        "z": 1,
        "x": 2,
        "c": 3,
        "v": 4,
        "b": 5,
        "n": 6,
        "m": 7
    }
    result = 0
    for letter in variant:
        letter_number = keyboard_distance[letter]
        result = result + letter_number
    return result


def string_similarity(original, variant):
    similarity = difflib.SequenceMatcher(isjunk=None, a=original, b=variant).ratio()
    return similarity


if __name__ == '__main__':

    # The excel file should contain three columns with the following titles: 'Screen Name', 'User Name', and 'Risk'.
    # This version is tailored to work on Twitter, so it is the Twitter screen name and user name that is acquired via
    # the API. Risk is manually assigned for the purposes of ML classification.
    df = pd.read_excel('filename.xlsx')
    # original screen name
    name = 'accountname'
    variations = df["Screen Name"].tolist()
    risks = df["Risk"].tolist()

    results = []
    original_difference = distance_difference(name)
    print('Keyboard Distance for ' + name + ' is: ' + str(original_difference))
    for variant, risk in zip(variations, risks):
        try:
            word = variant.lower()
        except AttributeError:
            print("Error with: " + str(variant))
            word = "error"

        # fuzzywuzzy module
        fuzzy_difference = fuzz.ratio(name.lower(), word.lower())
        fuzzy_partial_ratio = fuzz.partial_ratio(name.lower(), word.lower())
        fuzzy_token = fuzz.token_sort_ratio(name.lower(), word.lower())

        first_last_match = first_last_letter_match(name, word)
        difference_in_word_length = word_length_difference(name, word)
        name_in_variant = original_name_match(name, word)
        distance_of_keys = distance_difference(word)
        string_difflib = string_similarity(name, word)
        final_distance = distance_of_keys - original_difference
        wsong_distance = typoDistance(name, word, layout='QWERTY')

        # for weighting purposes
        if string_difflib < 0.5:
            add_letters = abs(letter_addition(word) - letter_addition(name))
            list_item = [name, word, risk, wsong_distance, abs(final_distance), abs(final_distance) + 10,
                         abs(final_distance) + add_letters, abs(final_distance) + add_letters,
                         fuzzy_difference, fuzzy_partial_ratio, fuzzy_token, first_last_match,
                         difference_in_word_length, name_in_variant]
        else:
            add_letters = abs(letter_addition(word) - letter_addition(name))
            list_item = [name, word, risk, wsong_distance, abs(final_distance), abs(final_distance),
                         abs(final_distance), abs(final_distance) + add_letters, fuzzy_difference,
                         fuzzy_partial_ratio, fuzzy_token, first_last_match, difference_in_word_length, name_in_variant]
        results.append(list_item)

    csvfile = open(name + '-metrics.csv', 'a', encoding="utf-8", newline='')
    writer = csv.writer(csvfile)
    writer.writerow(["Original Name", "Variant Screen Name", "Risk", "Wsong Keyboard Distance",
                     "Keyboard Distance without Weighting", "Keyboard Distance with Static Weighting",
                     "Keyboard Distance with Dynamic Weighting on Low Similarity",
                     "Keyboard Distance with Dynamic Weighting on All",
                     "Fuzzy Distance Ratio", "Fuzzy Partial Ratio", "Fuzzy Token Sort Ratio",
                     "First and Last Letter Match", "Word Length Difference", "Original Name in Variant"])

    for result in results:
        writer.writerow(result)
        print(result)