#!/usr/bin/env python3

import sys
import unittest


def parse_punch_card(card):
    row_values = "0123456789abcdef"

    lines = card.strip().split('\n')
    punched_rows = [line for line in lines if 'o' in line]

    result = ""
    col_starts = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60]

    for col in col_starts:
        chars = []

        for row in punched_rows:
            if row[col] == 'o':
                row_label = row[1]
                if row_label not in row_values:
                    continue

                chars.append(row_label)

        if 'c' in chars and len(chars) == 2:
            chars.remove('c')
            chars = [x.upper() for x in chars]

        if len(chars) > 1:
            return ""

        result += ''.join(chars)

    return result


def validate_punch_card(card):
    lines = card.strip().split('\n')

    if len(lines) != 20:
        return False

    if not lines[0].startswith("_") or not lines[-1].startswith("|_"):
        return False

    headers = lines[1].split()
    expected_headers = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e',
        'f'
    ]
    if headers[1:16] != expected_headers:
        return False

    for line in lines[3:-1]:
        if not line.startswith("|") or not line.endswith("|"):
            return False
        if len(line) != 63:
            return False

        row_label = line[1:3].strip()
        if row_label not in [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b',
                'c*', 'd', 'e', 'f'
        ]:
            return False

    return True


def main():
    card = ""
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        card += line
        if line.startswith(
                "|_____________________________________________________________|"
        ):
            if not validate_punch_card(card):
                return
            result = parse_punch_card(card)

            # If you make your last column c+e, you can send another card.
            done = not result.endswith("E")
            if not done:
                print(result[:-1], end='')
            else:
                print(result)
                break
            card = ""


test_input_1 = ("""
  ____________________________________________________________
 /  1   2   3   4   5   6   7   8   9   a   b   c   d   e   f |
/                                                             |
|0                      o                                     |
|1                              o       o                     |
|2                                                            |
|3                                                            |
|4      o       o                   o                         |
|5                                                            |
|6                                                            |
|7                                                            |
|8                                                            |
|9                                                            |
|a  o       o                                                 |
|b                                                            |
|c* o       o       o       o                                 |
|d                  o                                         |
|e                                                            |
|f                          o                                 |
|_____________________________________________________________|
""", 'A4A4D0F141')

test_input_2 = ("""
  ____________________________________________________________
 /  1   2   3   4   5   6   7   8   9   a   b   c   d   e   f |
/                                                             |
|0          o       o                                         |
|1                                                            |
|2                                                            |
|3                                                            |
|4                                                            |
|5                                                            |
|6                                                            |
|7                                                            |
|8                                                            |
|9      o                                                     |
|a  o                   o                                     |
|b                          o                                 |
|c* o           o               o                             |
|d                                  o                         |
|e                                                            |
|f              o                                             |
|_____________________________________________________________|
""", 'A90F0abcd')


# Defining the unittests with the corrected input strings
class TestPunchCardParser(unittest.TestCase):
    def test_parser_1(self):
        self.assertEqual(parse_punch_card(test_input_1[0]), test_input_1[1])

    def test_parser_2(self):
        self.assertEqual(parse_punch_card(test_input_2[0]), test_input_2[1])


if __name__ == "__main__":
    #unittest.main()
    main()
