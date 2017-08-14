# 2ch wipe tool
Заставь модератора работать
# Как запустить
Установите PIL для работы с картинками
```
sudo pip3 install Pillow
```
И запускайте одним из следующих способов
```
python3 main.py b 0 100       # вайпает доску /b/ в 100 потоков
python3 main.py b 12345 100   # вайпает тред 12345 на доске /b/ в 100 потоков
```
# Как настроить
138 и 139 строчки:
```
self.solver = CaptchaSolver_anticaptcha("anti-captcha.com api key")
# self.solver = CaptchaSolver_rucaptcha("rucaptcha.com api key")
```
Раскомментируйте вторую строчку и закомментируйте первую, если хотите использовать сервис rucaptcha.com. Не забудьте указать свой API-ключ
  
150 и 151 строчки:
```
post.set_text("**ALLO YOBA ETO TI**")  # Текст поста
post.set_image("./yoba.png", "blob")   # Картинка поста и её отображаемое имя
```
Не забудьте добавить прокси в файл proxies  
Можете рандомизировать текст с помощью модуля [markovify](https://github.com/jsvine/markovify)


По всем вопросам пишите в телеграм [@glow_stick](https://t.me/glow_stick), по возможности буду отвечать
