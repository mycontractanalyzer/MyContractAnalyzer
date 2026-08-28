TARIFFS = {
    "Free": {"price": 0, "checks": 1, "limit_chars": 15_000},
    "Starter": {"price": 249, "checks": 15, "limit_chars": 35_000},
    "Standard": {"price": 499, "checks": 50, "limit_chars": 65_000},
    "Pro": {"price": 899, "checks": 100, "limit_chars": 125_000},
    "Business": {"price": 2990, "checks": 250, "limit_chars": 175_000},
    "Business Pro": {"price": 5990, "checks": 400, "limit_chars": 250_000},
}

DISPLAY_NAMES = {
    "Free": "Пробный",
    "Starter": "Стартовый",
    "Standard": "Стандартный",
    "Pro": "Pro",
    "Business": "Бизнес",
    "Business Pro": "Business Pro",
}

PERIOD_DISCOUNTS = {1: 0.0, 3: 0.05, 6: 0.10, 9: 0.10, 12: 0.20, 24: 0.30}

FEATURES = {
    "Free": ["Модель Flash (быстрая)", "Базовый анализ"],
    "Starter": ["Модель Pro (глубокая)", "Полный анализ с флагами", "Чат с ИИ"],
    "Standard": ["Модель Pro", "Полный анализ", "Чат с ИИ", "Отчет в формате PDF"],
    "Pro": ["Модель Pro", "Детальный анализ + самопроверка", "Чат с ИИ", "Отчет в формате PDF"],
    "Business": ["Всё из Pro", "До 5 аккаунтов для компании", "Общая статистика проверок", "Приоритетная поддержка"],
    "Business Pro": ["Всё из Pro", "До 20 аккаунтов для компании", "Статистика и отчеты по команде", "Максимальные лимиты", "Приоритетная поддержка"],
}


def price_for(tariff: str, months: int) -> int:
    base = TARIFFS[tariff]["price"] * months
    discount = PERIOD_DISCOUNTS.get(months, 0.0)
    return int(base * (1 - discount))