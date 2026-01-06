"""
translation.py

문장 단위 영어 → 한국어 번역
"""

from app.services.llm import call_llm


def translate_sentence(sentence: str) -> dict:
    """
    영어 문장을 한국어로 번역한다.

    Args:
        sentence (str): 영어 문장

    Returns:
        dict:
        {
          "sentence_ko": "..."
        }
    """

    prompt = f"""
You are a professional English-Korean translator.

Translate the following English sentence into natural Korean.

Rules:
- Keep the meaning accurate.
- Sound natural to a Korean learner.
- Do NOT explain anything.
- Output must be valid JSON only.

English sentence:
"{sentence}"

Output format:
{{
  "sentence_ko": "..."
}}
"""

    return call_llm(prompt)
