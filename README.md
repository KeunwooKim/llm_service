# llm_service

Hugging Face에서 **원하는 LLM을 만들어 Hub에 올리는** 저장소입니다. 처음부터 사전학습하지 않고, 공개 베이스 모델을 내 데이터로 미세조정합니다.

**전체 정리:** [docs/llm.md](docs/llm.md) — 목표, 폴더, 8단계 파이프라인, 데이터 형식, 모델 후보. 노션에는 그 파일을 Import하거나 붙여넣은 뒤 `/목차`를 치면 됩니다.

코딩테스트 노트는 [docs/coding-test.md](docs/coding-test.md)에 그대로 있습니다. LLM 학습 데이터로 쓰지 마세요.

## 지금 상태

학습·업로드 코드는 아직 없습니다. 설정과 단계만 있습니다.

| 채워야 할 것 | 파일 |
| --- | --- |
| 한 줄 목표, system 프롬프트, Hub 이름 | `configs/llm.json` |
| 학습 JSONL 형식 | `data/samples/example.jsonl` |
| 단계 목록 | `python3 -m llm` |

```bash
cd llm_service
PYTHONPATH=src python3 -m llm
python3 -m unittest discover -s tests -v
```

`goal` / `system_prompt` / `hub_repo`가 비어 있으면 다음 구현을 시작하지 않습니다.

## 기본 선택 (바꿀 수 있음)

- 베이스: `Qwen/Qwen2.5-1.5B-Instruct`
- 학습: LoRA (VRAM이 부족하면 QLoRA)
- 데이터: `messages` JSONL (TRL SFTTrainer 형식)

## 폴더

```
configs/llm.json     한곳 설정
data/samples/        형식 예시
data/raw/            원본 (깃 무시)
data/processed/      학습용 JSONL (깃 무시)
src/llm/             설정·스키마·단계
docs/llm.md          전체 정리
outputs/             체크포인트 (깃 무시)
```
