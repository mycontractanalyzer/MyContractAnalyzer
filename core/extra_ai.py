import config
from core.analyzer import choose_model
from core.prompts import (build_lawyer247_prompt, build_podcast_prompt,
                          build_policy_prompt, build_precedent_prompt,
                          build_twin_prompt)
from integrations.deepseek import ask_deepseek


def analyze_policy(text, tariff):
    return ask_deepseek(build_policy_prompt(),
                        f"УСЛОВИЯ ПОЛИСА:\n\n{text[:15000]}", config.MODEL_FREE)


def lawyer247(question, tariff, history=""):
    return ask_deepseek(build_lawyer247_prompt(history), question, choose_model(tariff))


def twin_answer(question, user, reports):
    return ask_deepseek(build_twin_prompt(user, reports), question, choose_model(user["tariff"]))


def generate_podcast(topic):
    return ask_deepseek(build_podcast_prompt(), f"Тема выпуска: {topic}", config.MODEL_FREE)


def generate_precedent(text, report, tariff):
    return ask_deepseek(build_precedent_prompt(),
                        f"ДОГОВОР:\n\n{text[:15000]}\n\nОТЧЁТ:\n\n{report[:6000]}",
                        choose_model(tariff))