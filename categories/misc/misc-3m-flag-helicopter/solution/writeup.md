# Helicopter

| Cобытие       | Название       | Категория | Сложность |
|:-------------:|:-------------: |:---------:|:---------:|
| VKACTF 2024 | Helicopter | Misc | Сложная |

## Описание

>Автор [EGM]
>
>Вертолеты, кругом вертолеты! Надо торопиться, чтобы пройти эту миссию! Вспомни как это было в детстве.

# Решение

1. Изучив код сервера можно понять, что взаимодействие происходит только через ввод имени.

player_name = bytes.fromhex(input("Enter name in hex format: "))
HeroName(io.BytesIO(player_name)).load()
```
2. Ввод происходит через класс HeroName() 
class HeroName(pickle.Unpickler): 
     def find_class(self, module, name): 
        if module == 'collections' and '__' not in name:
            return getattr(collections, name)
        raise pickle.UnpicklingError('bad')
```

3. Таким образом, переопределяя атрибут в модуле collections, можно получить rce на сервер.

4. Ввод данных на сервер происходит в hex режиме, для этого экплойт переводим в байт код pickle. Можно использовать "pickora".
```
pickora splo.py -f hex
```
5. Отправляем последовательность на сервер и получаем флаг. 

### Эксплоит

[exploit.py](../give/hell_exploit.py)

### Флаг
```
vka{h3l1c0pTer_HeliCoPt3r_pAra_k0f3r_PaRa_KoF3r}

```
