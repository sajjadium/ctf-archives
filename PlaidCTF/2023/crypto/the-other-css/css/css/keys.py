import os

authentication_key = bytes.fromhex(os.environ["CSS_AUTHENTICATION_KEY"])
assert len(authentication_key) == 8

player_key_id = int(os.environ["CSS_PLAYER_KEY_ID"])
player_key_data = bytes.fromhex(os.environ["CSS_PLAYER_KEY_DATA"])
assert 0 <= player_key_id <= 255
assert len(player_key_data) == 8
player_key = (player_key_id, player_key_data)
