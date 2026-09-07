import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.laws_autoload import DEFAULT_PACK, autoload_law

for prefix, title, cands in DEFAULT_PACK:
    n, err = autoload_law(prefix, title, cands)
    print(f"{title}: {n if n else err}")