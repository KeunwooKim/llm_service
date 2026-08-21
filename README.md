# Screen solver

맥북 전체 화면을 1분마다 캡처하고, Cursor Agent가 스크린샷에서 프로그래밍 문제를 찾아 **파이썬 위주 정답**과 **다른 답변**을 저장합니다.

이 프로그램은 **본인 맥의 화면**을 대상으로 합니다. 시험·과제 부정행위용이 아니라, 화면에 보이는 문제를 학습용으로 풀이하는 도구입니다. 화면에는 비밀번호와 개인정보가 들어갈 수 있으니 저장 폴더를 공유하지 마세요.

## 동작

1. macOS `screencapture`로 전체 화면을 PNG로 저장 (`captures/`)
2. 이전 프레임과 같으면 분석을 건너뜀
3. Cursor Agent CLI(`agent -p --mode ask`)가 이미지를 읽고 문제를 판별
4. 언어/구현 문제면 파이썬 정답 + 대안 풀이 2개 이상을 `solutions/`에 저장

Cursor 창에서 직접 분석하려면 캡처만 돌린 뒤, 채팅에 `captures/latest.png`를 넣고 “이 화면의 프로그래밍 문제를 풀어줘”라고 하면 됩니다. 프로젝트 규칙이 같은 기준을 씁니다.

## 맥북 준비

1. **Python 3.10+**
2. **화면 기록 권한**: 시스템 설정 → 개인정보 보호 및 보안 → 화면 기록에서 `Terminal`, `iTerm`, 또는 `Cursor`를 허용
3. **Cursor Agent CLI** (자동 분석 시):

```bash
curl https://cursor.com/install -fsS | bash
agent login
```

## 실행

저장소를 받은 뒤, 이 폴더에서 실행합니다. 별도 패키지 설치는 필요 없습니다.

```bash
cd /path/to/this-repo
PYTHONPATH=src python3 -m screen_solver
```

기본은 **60초 간격**입니다.

| 목적 | 명령 |
| --- | --- |
| 1분마다 캡처 + Cursor 분석 | `PYTHONPATH=src python3 -m screen_solver` |
| 한 번만 | `PYTHONPATH=src python3 -m screen_solver --once` |
| 캡처만 (Cursor 창에서 직접 분석) | `PYTHONPATH=src python3 -m screen_solver --capture-only` |
| 이미 있는 이미지 분석 | `PYTHONPATH=src python3 -m screen_solver --once --image ./captures/latest.png` |
| 간격 변경 | `PYTHONPATH=src python3 -m screen_solver --interval 60` |

결과는 `captures/latest.png`와 `solutions/latest.md`에 덮어 씁니다. 타임스탬프 파일은 최근 60개만 남깁니다.

## Cursor 창에서만 쓰기

1. `PYTHONPATH=src python3 -m screen_solver --capture-only` 로 스크린샷만 쌓기
2. Cursor에서 이 폴더를 연 다음 `captures/latest.png`를 채팅에 첨부
3. 에이전트가 파이썬 정답과 다른 답변을 작성

## 테스트

```bash
python3 -m unittest discover -s tests -v
```
