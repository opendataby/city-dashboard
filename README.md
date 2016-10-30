# city-dashboard
City dashboard for Minsk using open datasets/  
Приборная доска города Минска на открытых датасетах

# Как подключится к процессу

Можно редактировать онлайн (просто, но неудобно), а можно
пользоваться git (удобно, но не просто).

В любом случае на вашей машине должен [стоять ruby](https://ru.wikibooks.org/wiki/Ruby/%D0%9D%D0%B0%D1%87%D0%B0%D0%BB%D0%BE_%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%8B/%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0) и git, чтобы видеть
результат своей работы.

* Скачиваете код:

      git clone git@github.com:opendataby/city-dashboard.git

* Устанавливаете jekyll и запускаете локальный сервер:
```
cd city-dashboard
bundle install
bundle exec jekyll serve
# => Открываем в браузере http://localhost:4000
```

Все готово чтобы вносить изменения.

Чтобы отослать свои обновления, надо "форкнуть репозиторий" под своим именем, и залить в него изменения:
```
git push git@github.com:своёимя/city-dashboard.git
```

После этого зайти на сайт и нажать кнопочку "Create pull request" (или как-то так).

Больше информации здесь https://help.github.com/articles/syncing-a-fork/

Когда все готово, пушим в свой репозиторий `git push`, после чего в своем репозитории на github Pull requests > New pull request. Новый пул реквест дожен появится в основном репозитории, после того как его проверят и примут ваши изменения появятся на сайт https://opendataby.github.io/city-dashboard

По всем вопросам относительно информации из этого раздела можете смело писать на konstantin.reido@gmail.com

# Ссылки
[Ответы на вопросы](https://github.com/opendataby/city-dashboard/blob/master/docs/faq.md)

