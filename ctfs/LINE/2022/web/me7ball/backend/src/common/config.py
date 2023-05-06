import os
import random

import yaml

current_dir = os.path.join(os.path.dirname(__file__), "../../conf/")

class Config(object):
    """set app config in here"""
    SECRET_KEY = os.urandom(12).hex()
    JSON_AS_ASCII = False


def merge_dicts(dict1, dict2) -> dict:
    """
    Recursively merges dict2 into dict1
    :param dict1:
    :param dict2:
    :return:
    """
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return dict2
    for k in dict2:
        dict1[k] = merge_dicts(dict1[k], dict2[k]) if k in dict1 else dict2[k]
    return dict1


def load_env() -> str:
    env = os.environ.get("FLASK_ENV")
    if env is None:
        return "development"
    return os.environ.get("FLASK_ENV")


def load_config() -> dict:
    """
    load conf based on environment
    :return:
    """
    try:
        with open(current_dir + "config.yaml", "r", encoding="utf-8") as conf_main:
            conf = (yaml.safe_load(conf_main))
        env = "dev"
        if os.environ.get("SCRIPT_ENV") == "production":
            env = "prod"
        elif os.environ.get("SCRIPT_ENV") == "staging":
            env = "staging"
        with open(current_dir + "config_%s.yaml" % env, "r", encoding="utf-8") as conf_f:
            conf = merge_dicts(conf, yaml.safe_load(conf_f))
        return conf
    except FileNotFoundError:
        return {}
