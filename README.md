# IOT
빌드 및 실행 명령어
docker compose -f docker-compose.dev.yml up --build

컨테이너 종료 및 삭제 명령어
docker compose -f docker-compose.dev.yml down

실시간 로그 확인(Ctrl + C 로 종료)
docker compose -f docker-compose.dev.yml logs -f

# 배포
빌드 및 실행 명령어
docker compose up --build -d

컨테이너 종료 및 삭제 명령어
docker compose down

로그 확인
docker compose logs -f