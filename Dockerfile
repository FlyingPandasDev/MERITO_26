FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

WORKDIR /app

COPY llm/requirements.txt /tmp/requirements.txt

RUN python - <<'PY'
from pathlib import Path

source = Path('/tmp/requirements.txt')
raw = source.read_bytes()

text = None
for encoding in ('utf-8', 'utf-16', 'utf-16-le', 'utf-16-be'):
    try:
        text = raw.decode(encoding)
        break
    except UnicodeDecodeError:
        continue

if text is None:
    raise UnicodeDecodeError('unknown', raw, 0, 1, 'Could not decode requirements file')

Path('/tmp/requirements.utf8.txt').write_text(text, encoding='utf-8')
PY

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.utf8.txt

COPY . /app

EXPOSE 8501

CMD ["sh", "-c", "streamlit run llm/llmFrontApp.py --server.address=0.0.0.0 --server.port=${PORT:-8501}"]