"""
Utility to format (to `str`) datetime.timedelta,
because I have found myself repeating this in several different projects.

mimicking datetime.strftime() formats:
Directive
%f: milliseconds
%s, %S: seconds
%m, %M: minutes
%h, %H: hours
%d, %D: days
The capital letter indicates that that would be the 'leading' term,
and would not be further divmod.

Let's say we have d=2, h=2, and we format to only to "%H:%m",
=> "50:00".

As the first implementation, there is not a lot of smart check inside,
e.g. if you do "%H:%s", the minutes will not converted to the "H" nor the "s".

To have a literal "%" character, use "%%".
"""

from datetime import timedelta
from math import floor
from typing import Final, List, Optional, Dict, Any, Union, Iterator

_directives2f_str: Final = {"f": "{f:03.0f}",
                      "s": "{s:02.0f}",
                      "m": "{m:02.0f}",
                      "h": "{h:02.0f}",
                      "d": "{d:.0f}",
                      "S": "{S:.0f}",
                      "M": "{M:.0f}",
                      "H": "{H:.0f}",
                      "D": "{D:.0f}"}


def _get_leading_chars(d_keys: List[str], ret_iterator=False) -> Union[List[str], Iterator[str]]:
    ret = filter(lambda x: x in "SMHD", d_keys)
    if ret_iterator:
        return ret
    else:
        return list(ret)


def _validate_and_ret_leading_char(d_keys: List[str]) -> str:
    leadings = _get_leading_chars(d_keys)
    assert(len(leadings) == 1), f"There are more than 1 leading terms: {leadings}"
    return leadings[0]


def formatTimedelta(td: timedelta, fmt: str) -> str:
    f_str, d_keys = _parse_fmt_string(fmt)
    fmt_kwargs = td_to_dict(td)
    leading = _validate_and_ret_leading_char(d_keys)
    if td < timedelta(0):
        fmt_kwargs[leading] *= -1
    return f_str.format(**fmt_kwargs)


def td_to_dict(td: timedelta, keys: Optional[List[str]] = None) -> Dict[str, float]:
    """
    Convert timedelta to a dict that can be used for formatting
    :param td:
    :param keys:
    :return:
    """
    f = td.microseconds / 1000
    S = abs(td.total_seconds())
    M, s = divmod(S, 60)
    s = floor(s)
    S = floor(S)
    H, m = divmod(M, 60)
    D, h = divmod(H, 24)
    d = D
    ret_dict: Dict[str, float] = dict(f=f, s=s, m=m, h=h, d=d, S=S, M=M, H=H, D=D)
    if keys is None:
        return ret_dict
    else:
        assert(all(key in ret_dict for key in keys)), f"Invalid key(s) in {keys}!"
        return {key: ret_dict[key] for key in keys}


def _parse_fmt_string(fmt: str) -> (str, List[str]):
    is_directive: bool = False
    d_keys: List[str] = []
    f_str: List[str] = []
    lat_recorded_str_idx: int = 0

    for i, char in enumerate(fmt):
        if is_directive:
            if char == "%":
                f_str.append("%")
            else:
                assert (char in _directives2f_str), f"Invalid directive '%{char}'!"
                d_keys.append(char)
                f_str.append(_directives2f_str[char])
            is_directive = False
            lat_recorded_str_idx = i + 1

        elif char == r"%":
            is_directive = True
            f_str.append(fmt[lat_recorded_str_idx:i])
            continue

    f_str.append(fmt[lat_recorded_str_idx:])
    return "".join(f_str), d_keys


if __name__ == '__main__':
    a = formatTimedelta(timedelta(days=2, hours=4, minutes=35, seconds=21), "%H:%m:%%%s")
    b = formatTimedelta(-timedelta(days=2, hours=4, minutes=35, seconds=21), "%H:%m:%s")

    print(a)
    print(b)

    kw = {'days': 29, 'seconds': 50, 'milliseconds': 774, 'minutes': 38, 'hours': 12}
    fmt = '%S blabla %f'
    c = formatTimedelta(timedelta(**kw), fmt)
    print(c)

