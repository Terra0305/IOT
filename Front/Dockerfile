# --- 1단계: 빌드(Build) 스테이지 ---
# 'as build'는 이 단계를 'build'라는 이름으로 참조할 수 있게 합니다.
# node:18-alpine을 사용하여 가볍고 효율적인 빌드 환경을 만듭니다.
FROM node:18-alpine as build

# 컨테이너 내의 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app

# package.json과 package-lock.json 파일을 먼저 복사합니다.
# (소스코드보다 먼저 복사하여, 종속성이 변경되지 않았다면 캐시를 활용하기 위함)
COPY package*.json ./

# package.json에 명시된 모든 종속성을 설치합니다.
RUN npm install

# 현재 디렉토리의 모든 소스 코드를 컨테이너의 /app 디렉토리로 복사합니다.
COPY . .

# React/Vue/Angular 등의 앱을 프로덕션용 정적 파일로 빌드합니다.
# (결과물은 보통 /app/dist 또는 /app/build에 생성됩니다)
RUN npm run build

# --- 2단계: 서빙(Serve) 스테이지 ---
# 빌드가 완료되었으므로, Nginx를 사용하여 파일을 서빙할
# '프로덕션용' 경량 이미지를 새로 시작합니다.
FROM nginx:alpine

# 'build' 스테이지(1단계)의 /app/dist 디렉토리에서
# Nginx의 기본 HTML 서빙 디렉토리로 빌드 결과물(정적 파일)만 복사합니다.
COPY --from=build /app/dist /usr/share/nginx/html

# Nginx가 80번 포트에서 리슨하도록 사용자 정의 설정을 복사합니다.
# (React Router 등을 위한 설정이 포함될 수 있습니다)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 이 컨테이너가 80번 포트를 외부에 노출할 것임을 명시합니다. (문서화 목적)
EXPOSE 80

# 컨테이너가 시작될 때 Nginx를 포어그라운드에서 실행합니다.
# ('daemon off;'는 컨테이너가 바로 종료되지 않게 합니다)
CMD ["nginx", "-g", "daemon off;"]