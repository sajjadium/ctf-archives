Author

pmsiam0

Hope you guys will enjoy it.

BASE62_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789" Add a shift within 1–93..

Note: Seed value is actually a key value.

Flag Format: KCTF{Fl4G_H3Re}

Hint: Phase One (Astra) – Each character’s ASCII value was turned into a base-62 string (letters/digits) separated by dashes. Phase Two (Equinox) – A pseudo-random shift was applied to each character (within printable ASCII range), controlled by a numeric seed.

The term “Astra” can metaphorically symbolize the act of mapping standard characters to a higher or “celestial” representation—here, it’s the conversion of ASCII values into base-62 strings. Think of it as elevating ordinary letters/numbers to a “starry” or more complex format. “Equinox” represents the cyclical nature of shifting characters. In astronomy, an equinox is when day and night are of equal length, marking a cycle. In the code, we apply a cyclical shift (with wrap-around) in the ASCII table, driven by a numeric seed.
