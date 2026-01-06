"""
sentence.py

유튜브 자막(transcript)을 '문장 단위' 학습 데이터로 변환한다.

핵심 설계 철학:
- 영어 학습은 '문단'보다 '문장'이 효율적이다.
- 자막은 불완전하므로, 규칙 기반 보정이 필요하다.
- 가능한 한 데이터를 버리지 않는다.
"""

from typing import List, Dict
import uuid


def split_transcript_into_sentences(
    transcript: List[Dict],
    time_gap_threshold: float = 3.0,
    min_sentence_length: int = 15,
) -> List[Dict]:
    """
    유튜브 자막 리스트를 문장 단위로 분리한다.

    문장 분리 기준:
    1. 문장 부호(. ? !)로 끝나는 경우
    2. 이전 자막과의 시간 간격이 일정 이상 벌어지는 경우
       → 화자가 바뀌거나 주제가 전환되었을 가능성이 큼

    Args:
        transcript: [{ "text": str, "start": float }]
        time_gap_threshold: 문장 분리 시간 기준 (초)
        min_sentence_length: 학습 가치가 있다고 판단하는 최소 길이

    Returns:
        [
          {
            "sentence_id": str,
            "start": float,
            "original": str
          }
        ]
    """

    sentences: List[Dict] = []

    # 현재 문장을 임시로 저장하는 버퍼
    buffer: List[str] = []

    # 현재 문장의 시작 시점
    sentence_start: float | None = None

    # 직전 자막의 시작 시점 (시간 간격 계산용)
    last_start: float | None = None

    for item in transcript:
        text: str = item["text"].strip()
        start: float = item["start"]

        # 문장 시작 시점 기록
        if sentence_start is None:
            sentence_start = start

        buffer.append(text)

        # ===== 문장 종료 판단 =====
        end_by_punctuation = text.endswith((".", "?", "!"))

        end_by_time_gap = (
            last_start is not None and
            start - last_start >= time_gap_threshold
        )

        end_of_sentence = end_by_punctuation or end_by_time_gap

        if end_of_sentence:
            full_sentence = " ".join(buffer).strip()

            # 너무 짧은 문장은 학습 가치가 낮으므로
            # 완전히 버리기보다는 조건부로만 저장
            if len(full_sentence) >= min_sentence_length:
                sentences.append({
                    # UUID 사용 → 정렬/필터링 변경에도 ID 안정
                    "sentence_id": str(uuid.uuid4()),
                    "start": sentence_start,
                    "original": full_sentence,
                })

            # 버퍼 초기화
            buffer = []
            sentence_start = None

        last_start = start

    # ===== 루프 종료 후 남은 버퍼 처리 =====
    if buffer and sentence_start is not None:
        full_sentence = " ".join(buffer).strip()
        if len(full_sentence) >= min_sentence_length:
            sentences.append({
                "sentence_id": str(uuid.uuid4()),
                "start": sentence_start,
                "original": full_sentence,
            })

    return sentences
