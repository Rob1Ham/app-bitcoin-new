from pathlib import Path
from typing import List, Dict, Any, Tuple
import re

from ledger_bitcoin.exception import DeviceException


SW_RE = re.compile(r"""(?x)
    \#                                 # character '#'
    define                             # string 'define'
    \s+                                # spaces
    (?P<identifier>SW(?:_[A-Z0-9]+)*)  # identifier (e.g. 'SW_OK')
    \s+                                # spaces
    0x(?P<sw>[a-fA-F0-9]{4})           # 4 bytes status word
""")


def parse_sw(path: Path) -> List[Tuple[str, int]]:
    if not path.is_file():
        raise FileNotFoundError(f"Can't find file: '{path}'")

    sw_h: str = path.read_text()

    return [(identifier, int(sw, base=16))
            for identifier, sw in SW_RE.findall(sw_h) if sw != "9000"]


def test_status_word(sw_h_path):
    expected_status_words: List[Tuple[str, int]] = parse_sw(sw_h_path)
    status_words: Dict[int, Any] = DeviceException.exc

    # just keep status words
    expected_status_words = [sw for (identifier, sw) in expected_status_words]

    # every app-defined status word must be mapped in DeviceException
    for sw in expected_status_words:
        assert sw in status_words, f"{hex(sw)} from sw.h not found in DeviceException mapping"

    # 0x5515 is SDK-defined and is allowed in addition to app-defined status words
    mapped_status_words = [sw for sw in status_words.keys() if sw != 0x5515]
    assert len(expected_status_words) == len(mapped_status_words), (
        f"{expected_status_words} doesn't match {status_words}")
