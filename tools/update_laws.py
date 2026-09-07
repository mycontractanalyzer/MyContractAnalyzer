"""
Автообновление базы законов.
Запускается по cron каждую неделю. Загружает недостающие законы,
перезаписывает существующие свежими редакциями.
"""
import os
import sys
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("update_laws")


def main():
    from database.connection import get_connection
    from core.laws_autoload import DEFAULT_PACK, autoload_law

    log.info("=== Начало автообновления базы законов ===")

    conn = get_connection()
    conn.execute("""CREATE TABLE IF NOT EXISTS laws (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE, title TEXT, essence TEXT,
        tags TEXT, category TEXT, full_text TEXT DEFAULT '')""")
    existing = {r[0] for r in conn.execute(
        "SELECT CASE WHEN instr(code,' ')>0 THEN substr(code,1,instr(code,' ')-1) ELSE code END FROM laws").fetchall()}
    conn.close()

    stats = {"loaded": 0, "articles": 0, "failed": 0}
    for prefix, title, cands in DEFAULT_PACK:
        if prefix in existing and prefix != "ГК":
            log.info("SKIP: %s уже в базе", title)
            continue
        n, err, source = autoload_law(prefix, title, cands)
        if err:
            log.error("FAIL: %s — %s", title, err)
            stats["failed"] += 1
        else:
            log.info("OK: %s — статей: %s (%s)", title, n, source)
            stats["articles"] += n or 0
            stats["loaded"] += 1

    log.info("=== Итог: загружено %s законов, %s статей, %s ошибок ===",
             stats["loaded"], stats["articles"], stats["failed"])


if __name__ == "__main__":
    main()