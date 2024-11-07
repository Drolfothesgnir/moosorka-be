@echo off
docker exec -t moosorka-be-db-1 pg_dump -U postgres diary > backup.sql