1. 실행 방법
이 프로젝트는 Docker Compose를 사용하여 '개발 환경'과 '운영 환경'을 분리하여 실행합니다.

2.1. 개발 환경 (Development)

개발 환경은 Dockerfile.dev를 사용하며, 코드 변경 시 서버가 자동으로 재시작됩니다.
빌드 명령어
docker build -t iot-backend-dev -f Dockerfile.dev .
실행 명령어
docker run -d -p 8000:8000 \
  -v .:/app \
  -e DATABASE_URL="postgresql://user:password@host.docker.internal:5432/weatherdb" \
  --name iot-backend-container \
  iot-backend-dev

환경 종료
docker stop iot-backend-container
docker rm iot-backend-container