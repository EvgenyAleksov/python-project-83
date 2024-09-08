### Hexlet tests and linter status:
[![Actions Status](https://github.com/EvgenyAleksov/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/EvgenyAleksov/python-project-83/actions)


[![Maintainability](https://api.codeclimate.com/v1/badges/4fabaa424b81c8bc239e/maintainability)](https://codeclimate.com/github/EvgenyAleksov/python-project-83/maintainability)


[![Actions Status](https://github.com/EvgenyAleksov/python-project-83/actions/workflows/pyci.yml/badge.svg)](https://github.com/EvgenyAleksov/python-project-83/actions)


[Посмотреть на render.com](https://python-project-83-fcn0.onrender.com/)


# Проект Вычислитель отличий

**Анализатор страниц** – это веб-сайт, который анализирует веб-страницы на предмет пригодности для SEO.


## Требования к установке
```
* Python 3.10.
* Poetry 1.8
```

## Установка

1. Склонировать репозиторий:
```
https://github.com/EvgenyAleksov/python-project-83.git
```

2. Прейти в директорию проекта:
```
cd python-project-83
```

3. Установить проект:
```
make install
```

4. В проекте имользуется База данных <a href="https://www.postgresql.org/" rel="nofollow">a database PostrgreSQL</a>.
Она должна быть установлена, и сервер запущен.


## Проверка кода проекта линтером _flake8_
```
poetry run flake8 page_analyzer
```


## Запуск
Локально:
```
make dev
```
