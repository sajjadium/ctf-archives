import os
import hashlib
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from skyfield.api import load

PRIME_BITS    = 512
TRUNCATE_BITS = 192
UNKNOWN_BITS  = PRIME_BITS - TRUNCATE_BITS
STEPS         = [0, 4, 10, 18, 28]
NUM_OUTPUTS   = len(STEPS)

EPOCH_YEAR  = 2026
EPOCH_MONTH = 1
EPOCH_DAY   = 26
EPOCH_HOUR   = __
EPOCH_MINUTE = __
EPOCH_SECOND = __

TAP_P = int(
    "B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C6"
    "9A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C0"
    "13ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD70"
    "98488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0"
    "A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708"
    "DF1FB2BC2E4A4371", 16)
TAP_Q = int("F518AA8781A8DF278ABA4E7D64B7CB9D49462353", 16)
TAP_G = int(
    "A4D1CBD5C3FD34126765A442EFB99905F8104DD2"
    "58AC507FD6406CFF14266D31266FEA1E5C41564B"
    "777E690F5504F213160217B4B01B886A5E91547F"
    "9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76"
    "A6A24C087A091F531DBF0A0169B6A28AD662A4D1"
    "8E73AFA32D779D5918D08BC8858F4DCEF97C2A24"
    "855E6EEB22B3B2E5", 16)


def load_comet_and_derive(year, month, day, hour, minute, second):
    from skyfield.data import mpc
    from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as GM_SUN

    with load.open('CometEls.txt') as f:
        comets = mpc.load_comets_dataframe(f)

    comets = comets.set_index('designation', drop=False)
    row = comets.loc['1P/Halley']

    ts = load.timescale()
    t = ts.utc(year, month, day, hour, minute, second)

    eph = load('de421.bsp')
    sun = eph['sun']
    halley = sun + mpc.comet_orbit(row, ts, GM_SUN)

    astrometric = sun.at(t).observe(halley)
    x, y, z = astrometric.position.au

    coord_string = f"{x:.10f}_{y:.10f}_{z:.10f}"
    h_a = hashlib.sha512((coord_string + "_A").encode()).digest()
    h_b = hashlib.sha512((coord_string + "_B").encode()).digest()
    return bytes_to_long(h_a), bytes_to_long(h_b)


def generate_telemetry(a, b, p):
    state         = bytes_to_long(os.urandom(PRIME_BITS // 8))
    outputs       = []
    current_index = 0

    for target_index in STEPS:
        for _ in range(target_index - current_index):
            state = (a * state + b) % p
        current_index = target_index
        outputs.append(state >> UNKNOWN_BITS)

    state = (a * state + b) % p
    return outputs, state


def tap_sign(step_indices, telemetry_values):
    x_tap = bytes_to_long(os.urandom(20)) % TAP_Q
    y_tap = pow(TAP_G, x_tap, TAP_P)

    k_tap = bytes_to_long(os.urandom(20)) % TAP_Q
    r_tap = pow(TAP_G, k_tap, TAP_P) % TAP_Q
    k_inv = pow(k_tap, -1, TAP_Q)

    sigs = []
    for step, t_val in zip(step_indices, telemetry_values):
        msg    = f"TAP:sector_{step}:{t_val}".encode()
        m_hash = int(hashlib.sha1(msg).hexdigest(), 16) % TAP_Q
        s_tap  = (k_inv * (m_hash + x_tap * r_tap)) % TAP_Q
        sigs.append((r_tap, s_tap))

    return y_tap, sigs


if __name__ == "__main__":
    if not os.path.exists('CometEls.txt'):
        import urllib.request
        urllib.request.urlretrieve(
            "https://minorplanetcenter.net/iau/Ephemerides/Comets/Soft00Cmt.txt",
            'CometEls.txt')

    a, b = load_comet_and_derive(
        EPOCH_YEAR, EPOCH_MONTH, EPOCH_DAY,
        EPOCH_HOUR, EPOCH_MINUTE, EPOCH_SECOND)

    p = getPrime(PRIME_BITS)
    telemetry, final_state = generate_telemetry(a, b, p)

    aes_key    = hashlib.sha256(long_to_bytes(final_state)).digest()
    iv         = os.urandom(16)
    cipher     = AES.new(aes_key, AES.MODE_CBC, iv)
    with open("flag.txt", "rb") as f:
        flag = f.read().strip()
    ciphertext = cipher.encrypt(pad(flag, AES.block_size))

    time_str   = f"{EPOCH_HOUR:02d}:{EPOCH_MINUTE:02d}:{EPOCH_SECOND:02d}"
    epoch_hash = hashlib.sha256(time_str.encode()).hexdigest()[:16]

    y_tap, sigs = tap_sign(STEPS, telemetry)

    with open("output.txt", "w") as f:
        f.write(f"Transmission Date   : {EPOCH_YEAR}-{EPOCH_MONTH:02d}-{EPOCH_DAY:02d}\n")
        f.write(f"epoch_hash          = {epoch_hash}\n")
        f.write(f"p = {p}\n")
        f.write("Telemetry (Broadcast Sectors):\n")
        for step, t_val in zip(STEPS, telemetry):
            f.write(f"  t_{step} = {t_val}\n")
        f.write(f"iv         = {iv.hex()}\n")
        f.write(f"ciphertext = {ciphertext.hex()}\n")
        f.write("\n[TAP Authentication Signatures]\n")
        f.write("  Sectors are signed by the spacecraft onboard DSA key (TAP v1.3, RFC 5114).\n")
        f.write(f"  tap_p = {TAP_P}\n")
        f.write(f"  tap_q = {TAP_Q}\n")
        f.write(f"  tap_g = {TAP_G}\n")
        f.write(f"  tap_y = {y_tap}\n")
        for step, (r, s) in zip(STEPS, sigs):
            f.write(f"  sig_t{step:02d} = (r={r}, s={s})\n")
