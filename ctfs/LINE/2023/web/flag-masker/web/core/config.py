from os import getenv


class Config:
    secret = getenv("secret")
    quries = {
        "write": "insert into memo (uid, memo, secret) values (:uid, :memo, :secret)",
        "loads": "select memo, secret from memo where uid = :uid",
    }
