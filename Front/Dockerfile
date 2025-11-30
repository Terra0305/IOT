# 1. Build Stage
FROM node:18-alpine as build

WORKDIR /app

# 패키지 파일 복사 및 설치
COPY package.json package-lock.json ./
RUN npm ci

# 소스 코드 복사
COPY . .

# 환경 변수 설정 (빈 문자열로 설정하여 상대 경로 사용 유도)
ENV VITE_APP_API_URL=""

# 빌드 실행 (Vite 빌드)
RUN npm run build

# 2. Production Stage (Nginx)
FROM nginx:alpine

# 빌드된 정적 파일 복사
COPY --from=build /app/dist /usr/share/nginx/html

# Nginx 설정 파일 복사
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 80번 포트 노출
EXPOSE 80

# Nginx 실행 (Foreground)
CMD ["nginx", "-g", "daemon off;"]
