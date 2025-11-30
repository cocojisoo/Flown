# Flown Frontend

React + TypeScript + Tailwind CSS 기반 프론트엔드 프로젝트

## 설치

```bash
npm install
```

## 개발 서버 실행

```bash
npm run dev
```

개발 서버는 `http://localhost:3000`에서 실행됩니다.

## 빌드

```bash
npm run build
```

## 미리보기

```bash
npm run preview
```

## 기술 스택

- **React 18** - UI 라이브러리
- **TypeScript** - 타입 안정성
- **Vite** - 빌드 도구
- **Tailwind CSS** - 유틸리티 우선 CSS 프레임워크

## 프로젝트 구조

```
frontend/
├── src/
│   ├── App.tsx          # 메인 앱 컴포넌트
│   ├── main.tsx         # 진입점
│   ├── index.css        # 전역 스타일 (Tailwind 포함)
│   └── vite-env.d.ts    # Vite 타입 정의
├── index.html           # HTML 템플릿
├── package.json         # 의존성 관리
├── tsconfig.json        # TypeScript 설정
├── vite.config.ts       # Vite 설정
├── tailwind.config.js   # Tailwind CSS 설정
└── postcss.config.js    # PostCSS 설정
```

## API 프록시

개발 환경에서 `/api/*` 요청은 자동으로 `http://localhost:8000`으로 프록시됩니다.

