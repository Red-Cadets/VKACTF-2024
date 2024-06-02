## GTSearch

| Событие | Название | Категория | Сложность |
| :------ | ---- | ---- | ---- |
| VKACTF 2024 | GTSearch  | Web | Средняя |

  
### Описание


> Автор: [ EGM ]
>
> Ты ничего не знаешь об этом городе? Воспользуйся этим поисковиком, он все тебе расскажет!


### Решение
1. Находим ```lfi``` используя поиск по файлам ```(байпас ../../)``` или используя абсолютный путь.

2. При переходе на ```/etc/passwd``` видим директорию откуда запущен файл.

3. При переходе на ```/proc/self/cmdline``` видим, что процесс запущен python3 server.py

4. Используя lfi на ```/home/app/server.py``` , получаем файл запускающий процесс 
```
from chal import server if __name__ == '__main__': server.run(host='0.0.0.0', port=10022)
```

5. Из вышеуказанного файла переходим на файл импорта ```/home/app/chal.py``` , получаем код сервера.

6. Изучив код и поняв, что есть endpoint возвращающий флаг, пробуем перейти на него. Получаем 403 ошибку nginx.

7. Внимательно посмотрев в код сервера и посмотрев на использующийся фрейворк flask и то, что сайт запущен без дополнительных серверов uvicorn, gunicron. Используем bypass 403 ошибки.
```
/8af2983d8ef4d16cd408b52cb5aaf1\x85
```

8. Проходим запрет nginx и получаем флаг. 

### Флаг

```
vka{4h_5h17_heR3_w3_g0_4g41n}
```