1. 실행 방법
이 프로젝트는 Docker Compose를 사용하여 '개발 환경'과 '운영 환경'을 분리하여 실행합니다.

2.1. 개발 환경 (Development)

개발 환경은 Dockerfile.dev를 사용하며, 코드 변경 시 서버가 자동으로 재시작됩니다.
빌드 명령어 및 실행 명령어
docker compose -f docker-compose.backend.dev.yml up --build

백그라운드 빌드 및 실행 명령어
docker compose -f docker-compose.backend.dev.yml up -d --build

실행 명렁어
docker compose -f docker-compose.backend.dev.yml up

실시간 로그 확인(Ctrl + C 로 종료)
docker compose -f docker-compose.backend.dev.yml logs -f

컨테이너 종료 및 삭제 명령어
docker compose -f docker-compose.backend.dev.yml down





