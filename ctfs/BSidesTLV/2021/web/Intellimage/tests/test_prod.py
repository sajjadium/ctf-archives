import unittest
import requests


class TestIntellimage(unittest.TestCase):
    def test_view(self):
        with open("VEVAK.png", "rb") as f:
            res = requests.post(
                url="http://localhost.realgame.co.il:5000/view",
                files={
                    "image[]": (
                        "VEVAK.png",
                        f.read(),
                        "image/jpeg"
                    ),
                },
                data={
                    "token": "4e4bad2093c856bfdabaf852d77c64bd06ec17a3"
                }
            )
        self.assertNotIn("error", res.json())
