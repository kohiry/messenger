# Мессенджер

Это веб приложение реализовывает простейший мессенджер.

## Технологии
Python, FastAPI, Alembic, SQLAchemy, Docker, Pytest, Makefile, Ruff

## Как запускать:
- На машине должен быть docker, docker-compose и make 
- запуск командой `make upd`


## Конечные точки:

### User
- GET `/api/user/profile/me`
- POST `/api/user/register`
- GET `/api/user/profile/{user_id}`
### Auth 
- POST `/api/security/token`
### Messanger
- GET `/api/chat/id/{chat_id}`
- GET `/api/chat/my`
- POST `/api/chat/start_with`
- POST `/api/chat/send_message`
### default
- GET `/`

