# 2ch wipe tool
Заставь модератора работать
# Как запустить
```
python main.py b 0 100       # вайпает доску /b/ в 100 потоков
python main.py b 12345 100   # вайпает тред 12345 на доске /b/ в 100 потоков
```
# Как настроить
136 и 137 строчки в main.py:
```
post.set_text("**ALLO YOBA ETO TI**")  # Текст поста
post.set_image("./yoba.png", "blob")   # Картинка поста и её отображаемое имя
```

Можете рандомизировать текст с помощью модуля [markovify](https://github.com/jsvine/markovify)

По всем вопросам пишите в телеграм [@glow_stick](https://t.me/glow_stick), по возможности буду отвечать
