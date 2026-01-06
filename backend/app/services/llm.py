"""
llm.py

Claude (Anthropic) LLM 공통 호출 모듈
- JSON 응답만 허용
- 번역 / 숙어 / 분석 공통 사용
"""

import os
import json
import re
from anthropic import Anthropic


# Anthropic 클라이언트 생성
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# 기본 모델 (가성비 + 안정성)
DEFAULT_MODEL = "claude-3-haiku-20240307"


class LLMResponseError(RuntimeError):
    """
    LLM 응답이 JSON 형식이 아니거나
    파싱에 실패했을 때 발생하는 에러
    """
    pass


def _extract_json(text: str) -> str:
    """
    Claude 응답에서 JSON 객체 부분만 추출한다.

    Claude는 종종:
    - 앞에 설명 문장
    - ```json ``` 코드블록
    을 포함하므로 이를 안전하게 제거한다.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise LLMResponseError("No JSON object found in Claude response")

    return match.group()


def call_llm(prompt: str, model: str = DEFAULT_MODEL) -> dict:
    """
    Claude에 프롬프트를 보내고
    JSON 응답을 dict로 반환한다.

    Args:
        prompt (str): LLM에게 전달할 프롬프트
        model (str): Claude 모델명

    Returns:
        dict: JSON 파싱된 결과
    """

    try:
        response = client.messages.create(
            model=model,
            max_tokens=512,
            temperature=0.2,  # 번역/분석은 낮게
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        # Claude 응답은 content 리스트 형태
        content_text = response.content[0].text.strip()

        # JSON 부분만 추출
        json_text = _extract_json(content_text)

        return json.loads(json_text)

    except json.JSONDecodeError as e:
        raise LLMResponseError("Invalid JSON format from Claude") from e

    except Exception as e:
        # 네트워크 / 인증 / API 오류 등
        raise RuntimeError("Claude API call failed") from e
