
# Развертывание task_API с PostgreSQL с использованием Docker


## Содержание

1. [Предварительные требования](#предварительные-требования)
2. [Шаги по установке](#шаги-по-установке)
3. [Запуск проекта](#запуск-проекта)
4. [Доступ к API](#доступ-к-api)


---

## Предварительные требования

Перед тем как начать развертывание, убедитесь, что у вас установлены следующие инструменты:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Шаги по установке

1. **Клонируйте репозиторий**

   Склонируйте репозиторий на ваш локальный компьютер:

   ```bash
   git clone https://github.com/vo1s/task_api.git
   cd your-repository-directory
   ```

2. **Настройте переменные окружения**

   Создайте файл `.env` в корневой директории проекта. В нем укажите параметры для вашей базы данных и суперпользователя, POSTGRES_DB оставьте таким же, какой в примере:

   ```ini
   POSTGRES_DB=template1
   POSTGRES_USER=_
   POSTGRES_PASSWORD=_
   PGADMIN_DEFAULT_EMAIL=_
   PGADMIN_DEFAULT_PASSWORD=_
   DJANGO_SUPERUSER_USERNAME=_
   DJANGO_SUPERUSER_EMAIL=_
   DJANGO_SUPERUSER_PASSWORD=_
   ```

---

## Запуск проекта

1. **Запустите контейнеры с помощью Docker Compose**

   В корневой директории проекта выполните команду:

   ```bash
   docker-compose up --build -d
   ```


2. **Проверьте, что все контейнеры работают**

   После того как контейнеры будут подняты, проверьте их статус:

   ```bash
   docker ps
   ```

   Убедитесь, что контейнеры `drf_app` и `db` запущены.



## Доступ к API

После успешного запуска проекта, вы сможете получить доступ к API на следующем URL:

```
http://localhost:8000/
```

Swagger доступен по:

```
http://localhost:8000/swagger
```

---

