# city-dashboard
City dashboard for Minsk using open datasets

# Как подключится к процессу

На вашей машине должен стоять ruby. Разбираемся с тем как его поставить.

* Форкаем проект и сливаем свой репозиторий к себе на машинку
* После этого нужно проделать следующее:
```
cd city-dashboard
bundle install
bundle exec jekyll serve
# => Открываем в браузере http://localhost:4000
```

Все готово чтобы вносить изменения.

Для того чтобы быть синхронизированным с основным репозиторием и получать обновления из него нужно проделать следующее:

* Это делаем один раз `git remote add upstream git@github.com:opendataby/city-dashboard.git`
* После этого каждый раз когда хотим слить последние изменения и смержить их со своими:
```
git fetch upstream
git merge upstream/master
```

Больше информации здесь https://help.github.com/articles/syncing-a-fork/

Когда все готово, пушим в свой репозиторий `git push`, после чего в своем репозитории на github Pull requests > New pull request. Новый пул реквест дожен появится в основном репозитории, после того как его проверят и примут ваши изменения появятся на сайт https://opendataby.github.io/city-dashboard

По всем вопросам относительно информации из этого раздела можете смело писать на konstantin.reido@gmail.com

