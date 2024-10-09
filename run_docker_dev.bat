@echo off
docker run -dp 5000:5000 -w /app -v "%cd%:/app" diary-app
