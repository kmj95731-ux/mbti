FROM python:3.11-slim
WORKDIR /app

# CPU 전용 PyTorch 먼저 설치 (GPU 버전 대비 이미지 ~1.3GB 절약)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 시맨틱 임베딩 모델 빌드 시 다운로드 → 런타임 콜드스타트 없음
RUN python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('jhgan/ko-sroberta-multitask')"

COPY . .
EXPOSE 7860
CMD ["python3", "-m", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "7860"]
