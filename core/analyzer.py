import config
from core.prompts import build_system_prompt
from integrations.deepseek import ask_deepseek


def choose_model(tariff: str) -> str:
    return config.MODEL_FREE if tariff == "Free" else config.MODEL_PAID


def analyze_contract(text, tariff="Free", contract_type="", role="", comment=""):
    model = choose_model(tariff)
    system = build_system_prompt(tariff, contract_type, role, comment)
    report = ask_deepseek(system, f"Вот текст договора для анализа:\n\n{text}", model)
    return report, model