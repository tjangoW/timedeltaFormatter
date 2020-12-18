"""
Fairly simple test over here
"""

import unittest
from datetime import timedelta
from random import randint
import random

from timedeltaFormatter import formatTimedelta


class TestTimedeltaFormatter(unittest.TestCase):

    def test_starter(self):
        self.assertEqual(formatTimedelta(timedelta(days=2, hours=4, minutes=35, seconds=21), "%H:%m:%%%s"), "52:35:%21")
        self.assertEqual(formatTimedelta(-timedelta(days=2, hours=4, minutes=35, seconds=21), "%H:%m:%s"), "-52:35:21")

    def test_random(self):
        seed = randint(0, 9999)
        print(f"random.seed({seed})")
        random.seed(seed)

        def char2f_str(char: str):
            if char.isupper():
                return f"{{{char}}}"
            else:
                return f"{{{char}:0{3 if char == 'f' else 2}}}"

        for i in range(50):
            f = randint(0, 1000 - 1)
            s = randint(0, 60 - 1)
            m = randint(0, 60 - 1)
            h = randint(0, 24 - 1)
            d = randint(0, 50 - 1)
            D = d
            H = h + D * 24
            M = m + H * 60
            S = s + M * 60
            fmt_kwargs = dict(f=f, s=s, m=m, h=h, d=d, D=D, H=H, M=M, S=S)

            td = timedelta(days=d, seconds=s, milliseconds=f, minutes=m, hours=h)

            # D0 H1 M2 S3 f4
            all_keys = "dhmsf"
            largest_i = randint(0, 3)
            big_key = all_keys.upper()[largest_i]
            small_keys = all_keys[largest_i + 1:5]
            fmt = f"%{big_key} blabla " + " - ".join("%" + key for key in small_keys)
            f_str = f"{char2f_str(big_key)} blabla " + " - ".join(char2f_str(key) for key in small_keys)

            self.assertEqual(formatTimedelta(td, fmt), f_str.format(**fmt_kwargs))
            # dict(days=d, seconds=s, milliseconds=f, minutes=m, hours=h)  to get value to debug

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
