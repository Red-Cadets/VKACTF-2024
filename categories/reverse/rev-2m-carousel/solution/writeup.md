# Santa-Maria Carousel

| Событие | Название | Категория | Сложность |
| :------ | ---- | ---- | ---- |
| VKACTF 2024 | Santa-Maria Carousel | Reverse | Средняя |


### Описание


> Автор: [b3rcut7]
>
> Привет. Ближе к делу. Мы выкрали шифровалку у Данангов, что-то типо Энигмы... Мы у них еще со стола шифр стащили, ломанёшь?
>


### Решение

```python
def scissors(input_str):
    return [input_str[i:i+2] for i in range(0, len(input_str), 2)]

def xor_str(input_str, key):
    string_list1 = scissors(input_str)
    string_list2 = scissors(key)
    result = ""
    for i in range(len(string_list1)):
        int1 = int(string_list1[i], 16)
        int2 = int(string_list2[i], 16)
        result += "{:02X}".format(int1 ^ int2)
    return result

def rotate_str(input_str, key):
    string_list = scissors(input_str)
    values = [string_list[(i + key) % len(string_list)] for i in range(len(string_list))]
    return "".join(values)

def decipher(cipher_text):
    initial_key = "77bb234face137c4ad1e61efc0f4f6eeee6f4f0cfe16e1da4c731ecaf432bb77"
    keys = []
    str_key = initial_key

    for i in range(0, len(str_key), 2):
        int_key = int(str_key[i:i+2], 16)
        keys.append(int_key)
        str_key = rotate_str(str_key, int_key)
    
    keys.reverse()

    input_str = cipher_text
    for key in keys:
        str_key = rotate_str(str_key, -key)
        input_str = xor_str(input_str, str_key)
    
    return input_str

cipher_text = 'B7B04EB788419838EEDEF75AAF9B4534A764AD7EF4AD4D943B3090F4968A72'
plain_text = decipher(cipher_text)
print("Original Text:", plain_text)
```

### Флаг

```
vka{YoU_4R3_CSH#RP_r3V_m4sT3r!}
```
