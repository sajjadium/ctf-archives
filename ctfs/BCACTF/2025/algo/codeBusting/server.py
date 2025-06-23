import sys
import json
import random
import time
import unicodedata

TIME_LIMIT = 15  # 15 seconds to solve em all!


def remove_accents_preserve_n(text):
    """
    Remove diacritics from text but preserve Ñ as its own character
    """
    result = []
    for char in text:
        if char in ["Ñ", "ñ"]:
            # Keep Ñ and ñ as they are
            result.append(char)
        else:
            # Remove accents from other characters
            # NFD = Normalization Form Decomposed
            normalized = unicodedata.normalize("NFD", char)
            # Filter out combining characters (accents)
            without_accents = "".join(
                c for c in normalized if unicodedata.category(c) != "Mn"
            )
            result.append(without_accents)
    return "".join(result)


def levenshtein_distance(s1, s2):
    """
    Calculate the Levenshtein distance between two strings
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    # Create a matrix to store distances
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions, or substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def normalize_text(text):
    """
    Normalize text for comparison by removing spaces and converting to lowercase
    """
    return "".join(text.lower().split())


def is_close(user_answer, correct_answer, max_errors=2):
    """
    Check if user answer is close to correct answer within max_errors
    """
    # Normalize both strings
    normalized_user = normalize_text(user_answer)
    normalized_correct = normalize_text(correct_answer)

    # Calculate edit distance
    distance = levenshtein_distance(normalized_user, normalized_correct)

    return distance <= max_errors


def key_s2tring_random(xeno):
    spl = lambda word: [char for char in word]
    if xeno:
        A = spl("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")
    else:
        A = spl("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    while not test1(A):
        random.shuffle(A)
    return "".join(A)


def test1(l):
    # Fixed: should check length properly for both regular and xenocrypt
    alphabet_size = len(l)
    for i in range(alphabet_size):
        if i < 14 and ord(l[i]) - 65 == i:
            return False
        elif (
            i > 14 and i < alphabet_size and ord(l[i]) - 65 == i - 1
        ):  # Account for Ñ offset
            return False
        elif i == 14 and l[i] == "Ñ":  # Ñ shouldn't be in its "natural" position
            return False
    return True


def getRandWord(minlen, maxlen):
    with open("words.txt", "r") as f:
        for _ in range(random.randint(0, 9000)):
            f.readline()
        r = ""
        while len(r) < minlen or len(r) > maxlen:
            r = f.readline().strip()
    return r


def genQuotes(n):
    l = open("quotes.txt", "r", encoding="utf-8").read().split("\n")
    random.shuffle(l)
    count = 0
    loc = 0
    r = []
    while count < n:
        if len(l[loc]) > 65 and len(l[loc]) < 160:
            r.append(l[loc])
            count += 1
        loc += 1
    return r


def genQuoteLength(minlen, maxlen):
    l = open("quotes.txt", "r", encoding="utf-8").read().split("\n")
    random.shuffle(l)
    loc = 0
    while 1:
        if len(l[loc]) > minlen and len(l[loc]) < maxlen:
            return l[loc]
        loc += 1


def genSpanishQuote(minlen, maxlen):
    data = json.load(open("spanish.json", "r"))
    l = [p["Cita"] for p in data["quotes"]]
    random.shuffle(l)
    loc = 0
    while 1:
        if len(l[loc]) > minlen and len(l[loc]) < maxlen:
            return l[loc][1:-1]
        loc += 1


def gen_rand_mono_pair(quote, pat):
    key = key_s2tring_random(False)
    r = {chr(i + 65): key[i] for i in range(26)}
    plaintext = quote.upper()
    ciphertext = "".join(r.get(c, c) for c in plaintext)
    return ciphertext, plaintext


def gen_rand_affine_pair(quote):
    a = random.choice([3, 5, 7, 9, 11, 15, 17, 19, 21, 23])
    b = random.randint(3, 24)
    plaintext = quote.upper()
    ciphertext = ""
    for c in plaintext:
        if "A" <= c <= "Z":
            ciphertext += chr((a * (ord(c) - 65) + b) % 26 + 65)
        else:
            ciphertext += c
    return ciphertext, plaintext


def gen_rand_caesar_pair(quote):
    a = random.randint(3, 24)
    plaintext = quote.upper()
    ciphertext = ""
    for c in plaintext:
        if "A" <= c <= "Z":
            ciphertext += chr((ord(c) - 65 + a) % 26 + 65)
        else:
            ciphertext += c
    return ciphertext, plaintext


def gen_rand_vig_pair(quote):
    key = getRandWord(5, 8).upper()
    plaintext = quote.upper()
    ciphertext = ""
    for i, c in enumerate(plaintext):
        if "A" <= c <= "Z":
            k = key[i % len(key)]
            ciphertext += chr((ord(c) - 65 + ord(k) - 65) % 26 + 65)
        else:
            ciphertext += c
    return ciphertext, plaintext


def genRandPorta_pair(quote):
    key = getRandWord(5, 8).upper()
    plaintext = quote.upper()
    ciphertext = ""
    for i, c in enumerate(plaintext):
        if "A" <= c <= "Z":
            k = key[i % len(key)]
            x = ord(c) - 65
            y = ord(k) - 65
            if y % 2 == 1:
                y -= 1
            if x < 13:
                ciphertext += chr(((x + y) % 26) + 65)
            else:
                ciphertext += chr(((x - y) % 26) + 65)
        else:
            ciphertext += c
    return ciphertext, plaintext


def gen_rand_xeno_pair():
    key = key_s2tring_random(True)
    quote = genSpanishQuote(70, 160)

    # Remove accents but preserve Ñ
    normalized_quote = remove_accents_preserve_n(quote)

    # Create mapping for 27-character Spanish alphabet
    r = {}
    # Map A-M to first 14 positions
    for i in range(14):
        r[chr(i + 65)] = key[i]
    # Map Ñ to 15th position (index 14)
    r["Ñ"] = key[14]
    # Map N-Z to remaining positions (indices 15-26)
    for i in range(14, 26):
        r[chr(i + 65)] = key[i + 1]

    plaintext = normalized_quote.upper()
    ciphertext = "".join(r.get(c, c) for c in plaintext)
    return ciphertext, plaintext


def generate_test_pairs():
    l = [
        "1 2",
        "1 1",
        "1 0",
        "1 1",
        "2 1",
        "2 2",
        "2 1",
        "2 0",
        "4 D",
        "4 E",
        "4 D",
        "4 E",
        "5 C",
        "8 1",
        "8 1",
        "8 1",
    ]
    n = len(l)
    q = genQuotes(n + 1)
    pairs = []
    ct, pt = gen_rand_mono_pair(q[-1], False)
    pairs.append((ct, pt))
    for i in range(n):
        question = l[i].split(" ")
        if int(question[0]) <= 2:
            ct, pt = gen_rand_mono_pair(q[i], question[0] == "2")
        elif int(question[0]) == 4:
            ct, pt = gen_rand_caesar_pair(q[i])
        elif int(question[0]) == 8:
            ct, pt = gen_rand_xeno_pair()
        pairs.append((ct, pt))
    return pairs


def main():
    with open("./flag.txt", "r") as file:
        FLAG = file.read().strip()
    pairs = generate_test_pairs()
    sys.stdout.write("Welcome to the Codebusting Challenge!\n")
    sys.stdout.write("Note: Answers are accepted with up to 2 character errors.\n")
    sys.stdout.flush()
    start_time = time.time()
    for idx, (ct, pt) in enumerate(pairs):
        # sys.stdout.write(f"plaintext is {pt}\n")  # debugging purposes
        sys.stdout.write(f"Ciphertext {idx+1}: {ct}\nYour answer: ")
        sys.stdout.flush()
        user = sys.stdin.readline().strip()
        if time.time() - start_time > TIME_LIMIT:
            sys.stdout.write("Time limit exceeded.\n")
            sys.exit(1)
        if is_close(user, pt, max_errors=2):
            if levenshtein_distance(normalize_text(user), normalize_text(pt)) > 0:
                sys.stdout.write(
                    f"Close enough! (Distance: {levenshtein_distance(normalize_text(user), normalize_text(pt))})\n"
                )
            continue
        else:
            distance = levenshtein_distance(normalize_text(user), normalize_text(pt))
            sys.stdout.write(
                f"Incorrect. Your answer was {distance} errors away (max allowed: 2).\n"
            )
            sys.exit(1)
    sys.stdout.write(f"Congratulations! Here is your flag: {FLAG}\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
