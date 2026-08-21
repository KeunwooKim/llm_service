# Screen solver

맥북 전체 화면을 1분마다 캡처하고, Cursor Agent가 스크린샷에서 프로그래밍 문제를 찾아 **파이썬 위주 정답**과 **다른 답변**을 터미널에만 출력합니다.

스크린샷·로그·해설 파일은 남기지 않습니다. 캡처는 시스템 임시 파일로만 만들고, 분석이 끝나면 바로 지웁니다. 프로그래밍 문제가 없으면 아무것도 출력하지 않습니다.

이 프로그램은 **본인 맥의 화면**을 대상으로 합니다. 시험·과제 부정행위용이 아니라, 화면에 보이는 문제를 학습용으로 풀이하는 도구입니다.

## 동작

1. macOS `screencapture -x`로 전체 화면을 임시 PNG로 찍음
2. 이전 프레임과 같으면 분석을 건너뛰고 임시 파일을 삭제
3. Cursor Agent CLI(`agent -p --mode ask`)가 이미지를 읽고 문제를 판별
4. 언어/구현 문제면 파이썬 정답 + 대안 풀이 2개 이상을 **표준 출력에만** 인쇄
5. 임시 스크린샷을 삭제. `captures/`, `solutions/`, `logs/` 를 만들지 않음

## 맥북 준비

1. **Python 3.10+**
2. **화면 기록 권한**: 시스템 설정 → 개인정보 보호 및 보안 → 화면 기록에서 `Terminal`, `iTerm`, 또는 `Cursor`를 허용
3. **Cursor Agent CLI**:

```bash
curl https://cursor.com/install -fsS | bash
agent login
```

## 실행

맥 터미널에서 저장소를 **기능 브랜치**로 받은 뒤 실행합니다. `main`에는 이 프로그램이 없습니다.

```bash
git clone -b cursor/mac-screen-solver-041f https://github.com/KeunwooKim/llm_service.git
cd llm_service
PYTHONPATH=src python3 -m screen_solver
```

이미 클론한 폴더가 있으면:

```bash
cd llm_service
git fetch origin
git checkout cursor/mac-screen-solver-041f
PYTHONPATH=src python3 -m screen_solver
```

| 목적 | 명령 |
| --- | --- |
| 1분마다 캡처 + 분석 | `PYTHONPATH=src python3 -m screen_solver` |
| 한 번만 | `PYTHONPATH=src python3 -m screen_solver --once` |
| 이미 있는 이미지 분석 | `PYTHONPATH=src python3 -m screen_solver --once --image ./example.png` |
| 간격 변경 | `PYTHONPATH=src python3 -m screen_solver --interval 60` |

`--image`로 넘긴 원본 파일은 지우지 않습니다. 프로그램이 만든 임시 캡처만 삭제합니다.

## 테스트

```bash
python3 -m unittest discover -s tests -v
```
