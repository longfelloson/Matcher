# Matcher (бот + сайт)

Проект для поиска новых знакомств.

## Бот

Бот для поиска новых знакомств. У пользователя есть возможность угадывать возраст анкеты других пользователей, за
каждый угаданный возраст анкеты, пользователь получает баллы, которые потом может обменять на маркете.

## Маркет

Маркет реализован на FastAPI. У пользователя есть возможность обменять баллы (**/exchange-points**)
на деньги, либо товары (**/add-user-product**).

## Установка на Linux

1) ```sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose```
2) ```sudo chmod +x /usr/local/bin/docker-compose```
3) ```docker compose + docker compose up```