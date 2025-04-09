### 종속성 설치

```bash
pip install -r requirements.txt
pip install -r requirements.test.txt
```

### 실행

```bash
# ollama 실행 옵션
# --ollama
# --ollama-url
# --ollama-model

# gemini 실행 옵션
# --gemini
# --gemini-key
# --gemini-model
# --source-path

python pytest_gen/pytest_gen_agent.py \
  --gemini \
  --gemini-key <키> \
  --gemini-model "gemini-2.0-flash"
```

### 종속성 기록

```bash
pipreqs --ignore bin,etc,include,lib,lib64 --force
```