import time
from typing import Dict

from server.game.entity.enemy import Enemy
from shared.constants import SERVER_TICK_RATE
from shared.gen.messages.v1 import AttackEnemy, User


class FightManager:
    user_damage_cooldowns: Dict[str, float]
    enemy_damage_cooldowns: Dict[str, float]

    def __init__(self) -> None:
        self.user_damage_cooldowns = {}
        self.enemy_damage_cooldowns = {}

    def can_take_damage_user(self, username: str, cooldown_ticks: int = 30) -> bool:
        # User not in list => Store and allow to take damage
        if not username in self.user_damage_cooldowns:
            self.user_damage_cooldowns[username] = time.time()
            return True

        last_damage_timestamp = self.user_damage_cooldowns[username]
        ticks_passed = (time.time() - last_damage_timestamp) * SERVER_TICK_RATE

        # Cooldown did not pass yet
        if ticks_passed < cooldown_ticks:
            return False

        self.user_damage_cooldowns[username] = time.time()

        return True

    def can_take_damage_enemy(self, enemy_uuid: str, cooldown_ticks: int = 30) -> bool:
        # User not in list => Store and allow to take damage
        if not enemy_uuid in self.user_damage_cooldowns:
            self.enemy_damage_cooldowns[enemy_uuid] = time.time()
            return True

        last_damage_timestamp = self.enemy_damage_cooldowns[enemy_uuid]
        ticks_passed = (time.time() - last_damage_timestamp) * SERVER_TICK_RATE

        # Cooldown did not pass yet
        if ticks_passed < cooldown_ticks:
            return False

        self.enemy_damage_cooldowns[enemy_uuid] = time.time()
        return True

    def is_plausible_attack(self, user: User, enemy: Enemy, attack_msg: AttackEnemy):
        # Check if attack direction is plausible:
        # TODO

        # Check if damage is plausible
        if attack_msg.damage > 11:
            return False

        if attack_msg.damage < 0:
            return False

        # Check if enemy is in range of weapon
        dist_x = (user.coords.x - enemy.x) ** 2
        dist_y = (user.coords.y - enemy.y) ** 2
        max_attack_distance = 400  # TODO: Find good value, maybe dynamic from weapon
        if dist_x + dist_y > max_attack_distance:
            return False

        attack_timestamp = time.mktime(attack_msg.time.timetuple())

        if not enemy.uuid in self.enemy_damage_cooldowns:
            self.enemy_damage_cooldowns[enemy.uuid] = attack_timestamp
            return True

        # TODO: Get dynamic from current user weapon
        weapon_cooldown_ticks = 30

        last_damage_timestamp = self.enemy_damage_cooldowns[enemy.uuid]

        ticks_passed = (attack_timestamp - last_damage_timestamp) * SERVER_TICK_RATE
        if ticks_passed > weapon_cooldown_ticks:
            self.enemy_damage_cooldowns[enemy.uuid] = time.mktime(
                attack_msg.time.timetuple()
            )

            return True
        return False
