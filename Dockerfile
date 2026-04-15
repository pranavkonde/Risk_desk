FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PACIFICA_NETWORK=testnet

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY riskdesk ./riskdesk
COPY streamlit_app.py .
COPY scripts ./scripts
COPY .streamlit ./.streamlit

USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=25s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=5)"

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", \
    "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
