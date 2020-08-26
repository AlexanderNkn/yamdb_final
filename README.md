# yamdb_final

![yamdb workflow status](https://github.com/AlexanderNkn/yamdb_final/workflows/yamdb/badge.svg)

Это REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке.

### Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор. 
Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя оценка произведения.

### Установка
- склонируйте проект с реппозитория GitHub
    ```
    git clone https://github.com/AlexanderNkn/yamdb_final.git
    ```
- перейдите в директорию yamdb_final/
    ```
    cd yamdb_final/
    ```
- запустите docker-compose
    ```
    docker-compose up
    ```

### Использование
- зайдите на страницу http://localhost:8000/redoc/ 
и воспользуйтесь документацией к API :smile:

### Дополнительные возможности
- заполнить базу тестовыми данными
    ```
    docker-compose run --rm web python manage.py loaddata fixtures.json
    ```
- создать суперпользователя
    ```
    docker-compose run --rm web python manage.py createsuperuser
    ```

