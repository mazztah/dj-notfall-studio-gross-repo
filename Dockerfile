# Stage 1: Frontend bauen (React + Vite)
FROM node:20 AS frontend
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY index.html vite.config.ts tsconfig.json tailwind.config.js postcss.config.js ./
COPY src/ ./src/
RUN npm run build

# Stage 2: Python + Gunicorn, serviert dist/ + API
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./
COPY --from=frontend /app/dist ./dist
EXPOSE 5000
CMD ["sh", "-c", "gunicorn -w 1 -b 0.0.0.0:$PORT app:app"]
