#Dockerfile

# 1. Python 3.10-slim 버전
FROM python:3.10-slim

#2. 작업 디렉토리
WORKDIR /app

# 3. requirements.txt를 먼저 복사하여 종속성 캐싱 활용
COPY requirements.txt .

# 3.5. RPi.GPIO 등 컴파일이 필요한 패키지를 위해 gcc 설치
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# 4. 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 나머지 소스 코드 복사
COPY . .

# 6. .env 파일은 Docker 이미지에 포함시키지 않습니다. (보안)
#    대신 docker-compose.yml의 'env_file'을 통해 런타임에 주입합니다.

# 7. 앱이 사용할 포트 (기본 8000)
EXPOSE 8000

# 8. Gunicorn을 사용하여 앱 실행
#    -k uvicorn.workers.UvicornWorker : Uvicorn을 워커로 지정 (ASGI 실행)
#     -b 0.0.0.0:8000 : 모든 인터페이스의 8000번 포트로 바인딩
#     -w 4 : 워커 프로세스 4개 (CPU 코어 수에 따라 조절)
#     main:app : main.py 파일의 app 객체를 실행
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "-w", "4", "main:app"]