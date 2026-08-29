import difflib


def diff_texts(old: str, new: str) -> str:
    """Возвращает человекочитаемый diff в виде HTML/markdown."""
    old_lines = old.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)
    diff = difflib.unified_diff(old_lines, new_lines, fromfile="Старая версия", tofile="Новая версия", lineterm="")
    return "".join(diff)


def summarize_diff(old: str, new: str) -> str:
    """Короткое текстовое описание: сколько строк добавлено/удалено."""
    old_set = set(old.splitlines())
    new_set = set(new.splitlines())
    added = len(new_set - old_set)
    removed = len(old_set - new_set)
    return f"Изменено: удалено строк — {removed}, добавлено строк — {added}."