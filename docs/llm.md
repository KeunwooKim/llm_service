# Hugging Face LLM 전체 정리

이 저장소의 다음 목표는 **원하는 LLM을 Hugging Face에서 만들고 Hub에 올리는 것**입니다. 처음부터 사전학습(pretrain)하지 않습니다. 공개 베이스 모델을 고른 뒤, 내 데이터로 지도 미세조정(SFT)하고, 필요하면 선호학습(DPO)을 붙입니다.

아직 **모델이 무엇을 잘해야 하는지**는 정해지지 않았습니다. 그 한 줄이 정해지기 전에는 학습 코드를 키우지 않습니다. 이 문서는 전체 그림과 리포 뼈대입니다.

> 노션: 이 파일을 Import → Markdown 하거나 붙여넣은 뒤 `/목차`를 치세요.

---

## 목차

- 한 줄 결정
- 하는 일 / 하지 않는 일
- 리포 구조
- 파이프라인 8단계
- 데이터 형식
- 모델 고르기
- 학습 방식
- 평가
- Hub에 올리기
- 서빙
- 지금 막힌 결정
- 코딩테스트 노트

### 빠른 찾기

| 키워드 | 위치 |
| --- | --- |
| 목표, 페르소나 | 한 줄 결정 |
| 폴더 | 리포 구조 |
| SFT, LoRA, QLoRA | 학습 방식 |
| messages, JSONL | 데이터 형식 |
| Qwen, 라이선스 | 모델 고르기 |
| push_to_hub | Hub에 올리기 |
| HF_TOKEN | 환경 |
| 코딩테스트 | docs/coding-test.md |

---

## 한 줄 결정

> 유형: 기획 / 필수

아래를 채우면 다음 구현이 시작됩니다. 설정 파일은 `configs/llm.json`입니다.

| 항목 | 지금 값 | 채워야 하는 것 |
| --- | --- | --- |
| 한 줄 목표 | (미정) | 예: 한국어로 짧은 코드를 설명하는 조수 |
| 말투·금지 | (미정) | system 프롬프트 초안 |
| 베이스 모델 | `Qwen/Qwen2.5-1.5B-Instruct` | 작아서 실험하기 좋음. 원하면 바꿔도 됨 |
| Hub 저장소 | (미정) | `계정이름/모델이름` |
| GPU | (미정) | VRAM GB. 없으면 데이터·평가만 |

처음부터 70B를 학습하지 않습니다. 작은 모델로 파이프라인을 통과시킨 뒤 키웁니다.

---

## 하는 일 / 하지 않는 일

> 유형: 범위

**하는 일**

1. 목표와 데이터 형식을 고정한다.
2. Hugging Face 베이스 모델을 고른다.
3. JSONL 대화 데이터로 SFT(LoRA/QLoRA) 한다.
4. 몇 개 프롬프트로 생성 품질을 본다.
5. 어댑터 또는 병합 모델을 Hub에 올린다.
6. 나중에 간단한 추론/서빙을 붙인다.

**하지 않는 일 (지금은)**

- 스크래치 사전학습 (데이터·돈·시간이 다른 규모)
- 저작권 있는 문제/책/코드를 학습 데이터로 넣기
- 토큰·키를 깃에 넣기
- 평가 없이 Hub에 올리기

코딩테스트 노트(`docs/coding-test.md`)는 학습 데이터가 아닙니다. 공부용으로 그대로 둡니다.

---

## 리포 구조

> 유형: 구조

```
llm_service/
  configs/llm.json          # 모델·데이터·Hub 한곳 설정
  data/raw/                 # 원본 (깃에 올리지 않음)
  data/processed/           # 학습용 JSONL (깃에 올리지 않음)
  data/samples/example.jsonl
  docs/llm.md               # 이 문서
  docs/coding-test.md       # 기존 코테 노트
  src/llm/                  # LLM 파이프라인 (지금은 설정·단계만)
  src/coding_test/          # 기존 코테 템플릿
  outputs/                  # 체크포인트 (깃에 올리지 않음)
```

파이썬 설정은 `src/llm/config.py`가 `configs/llm.json`을 읽습니다. 단계는 `src/llm/stages.py`에 순서대로 있습니다.

```bash
python3 -m llm                 # 단계 목록
python3 -m unittest discover -s tests -v
```

---

## 파이프라인 8단계

> 유형: 로드맵

| 단계 | 이름 | 산출물 | 지금 |
| --- | --- | --- | --- |
| 0 | 결정 | 한 줄 목표, Hub id, GPU | 대기 |
| 1 | 환경 | `HF_TOKEN`, 선택 의존성 | 대기 |
| 2 | 데이터 | `data/processed/train.jsonl` | 형식만 |
| 3 | 베이스 | Hub에서 토크나이저·모델 | 후보만 |
| 4 | SFT | LoRA 어댑터 | 미구현 |
| 5 | 평가 | 고정 프롬프트 생성 로그 | 미구현 |
| 6 | Hub | `push_to_hub` | 미구현 |
| 7 | 서빙 | 로컬 추론 또는 Space | 미구현 |

한 단계가 끝나야 다음 코드를 짭니다. 지금은 0~2를 채우는 단계입니다.

---

### 0. 결정

목표 문장 하나가 데이터와 평가를 정합니다.

- 좋은 예: “초심자에게 파이썬 에러 메시지를 한국어로 짧게 설명한다.”
- 나쁜 예: “똑똑한 만능 챗봇.”

라이선스: 베이스 모델 라이선스가 파생 모델에도 붙습니다. Qwen2.5는 대체로 연구·상업이 넓고, Llama는 게이트·조건이 있습니다. Hub 모델 카드의 License를 읽습니다.

---

### 1. 환경

```bash
# 나중에 학습을 붙일 때
pip install -e ".[llm]"
huggingface-cli login   # 또는 환경변수 HF_TOKEN
```

| 항목 | 규칙 |
| --- | --- |
| `HF_TOKEN` | `.env` 또는 셸. `.env`는 깃 무시 |
| 캐시 | `HF_HOME` 또는 기본 `~/.cache/huggingface` |
| GPU | CUDA가 있으면 QLoRA, 없으면 데이터 검증만 |

이 클라우드 VM에서 큰 모델 학습을 전제로 두지 않습니다. 학습은 GPU가 있는 쪽에서 같은 설정을 읽고 돌립니다.

---

### 2. 데이터

학습 한 줄은 대화 리스트입니다. TRL `SFTTrainer`가 `messages`를 보면 모델의 chat template을 적용합니다.

```json
{"messages":[{"role":"system","content":"짧은 한국어로 답한다."},{"role":"user","content":"NameError가 뭐야?"},{"role":"assistant","content":"이름 없는 변수를 쓸 때 납니다. 오타와 import를 먼저 보세요."}]}
```

규칙은 `src/llm/schema.py`와 `data/samples/example.jsonl`이 같습니다.

- `role`은 `system` / `user` / `assistant`만.
- 각 샘플에 `user`와 `assistant`가 최소 한 번씩.
- 원본은 `data/raw/`, 변환 결과는 `data/processed/`.
- 품질: 짧고, 목표와 같고, 중복·유출(개인정보·기출 원문) 없이.

양보다 목표에 맞는 수백~수천 건이 먼저입니다.

---

### 3. 베이스 모델

기본 후보는 작아서 파이프를 검증하기 좋은 모델입니다.

| 상황 | 후보 | 이유 |
| --- | --- | --- |
| 기본 실험 | `Qwen/Qwen2.5-1.5B-Instruct` | 한국어 가능, 작음, Hub에서 받기 쉬움 |
| 품질을 올릴 때 | `Qwen/Qwen2.5-7B-Instruct` | 같은 족보라 데이터 재사용 |
| 한국어 특화 | EXAONE, HyperCLOVA X 등 | 라이선스·게이트를 먼저 확인 |
| Llama 계열 | 3.2 1B/3B | Hugging Face 동의 필요 |

베이스는 **이미 Instruct인 것**을 고릅니다. Base만 있으면 지시 데이터를 훨씬 많이 써야 합니다.

---

### 4. 학습 (SFT)

> 유형: 학습

첫 학습은 전체 파인튜닝이 아니라 **LoRA**입니다. VRAM이 부족하면 **QLoRA**(4bit).

| 방식 | 언제 |
| --- | --- |
| LoRA | 대략 7B 이하, VRAM 여유 |
| QLoRA | 7B를 12GB 근처에서 |
| Full FT | 나중에, 이유가 있을 때만 |
| DPO/ORPO | SFT가 말투를 낸 뒤, 선호 쌍이 있을 때 |

스택(구현 때 설치): `transformers`, `datasets`, `trl`, `peft`, `accelerate`, `huggingface_hub`.

손실은 assistant 턴만 보는 쪽을 기본으로 합니다 (`assistant_only_loss`, 모델 chat template이 지원할 때).

체크포인트는 `outputs/`에만 씁니다. 깃에 올리지 않습니다. Hub가 배포본입니다.

---

### 5. 평가

숫자 벤치만 보고 올리지 않습니다. 목표에 맞는 **고정 프롬프트 10~20개**를 먼저 둡니다.

- 학습 전 베이스 출력
- 학습 후 출력
- 금지 행동(기출 원문 복붙, 개인정보) 나오는지

손실이 내려가도 말이 이상하면 데이터를 고칩니다. 학습률을 먼저 만지지 않습니다.

---

### 6. Hub에 올리기

```text
계정이름/내가-정한-모델이름
```

올릴 것: 어댑터(`adapter_model.safetensors` + `adapter_config.json`) 또는 merge한 전체 가중치, 토크나이저, `README.md`(모델 카드: 베이스, 데이터 개요, 라이선스, 의도된 사용).

비공개로 올렸다가, 평가가 끝나면 public으로 바꿉니다.

---

### 7. 서빙

학습이 통과한 뒤에만 붙입니다.

| 방법 | 용도 |
| --- | --- |
| `transformers` 로컬 generate | 개발 확인 |
| Hugging Face Space + Gradio | 데모 |
| Inference Endpoint / TGI | 나중에 API |

지금은 서빙 코드를 넣지 않습니다.

---

## 지금 막힌 결정

다음에 구현하려면 이 네 가지가 필요합니다.

1. **한 줄 목표** (무엇을 잘하게 할지)
2. **system 프롬프트 초안**
3. **Hub 저장소 이름** (`계정/모델`)
4. **학습할 기계** (로컬 GPU / Colab / 없음)

없으면 데이터 형식과 설정만 유지하고, 학습 스크립트는 쓰지 않습니다.

---

## 코딩테스트 노트

프로그래머스·SQL·개념 정리는 [coding-test.md](coding-test.md)에 그대로 있습니다. LLM 학습 코퍼스로 쓰지 마세요. 공식 기출 문장을 넣지 않은 것과 같은 이유입니다.
