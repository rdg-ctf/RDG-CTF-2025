Файлы:
`a25b8d0d6e82d8abc83d4cf80dc98738 magic.pyd`
`0e52b1ff681f11ff042a593c0392a9e6 pynja.py`


Файл `pynja.py`
---

Длина серийного номера - это `len(ins)` DWORD-ов. То есть в данном случае:

```
len(serial) == 50
```

Далее происходит сравнение по 4 байта массивов `serial` и `ins`:

```python
magic.Spell()
for idx, i in enumerate(serial):
	flag = (i == ins[idx])
	if not flag:
		print("[-] Wrong input")
		exit(-1)
magic.Dispell()
```

Из работы скрипта видно, что операция сравнения `i == ins[idx]` имеет отличное от стандартного поведение. Логично предположить, что переопределение происходит в модуле `magic`.

```python
magic.Spell()
# ...
	flag = (i == ins[idx])
# ...
magic.Dispell()
```

Файл `magic.pyd`
---

Экспорт `PyInit_magic` - инициализация `cpython` модуля, где обычно содержится указатель на `struct PyModuleDef` структуру, из которой можем достать адрес на список определенных в текущем модуле функций `PyMethodDef`.

![alt text](assets\image-1.png)

Также подмечаем, что при инициализации происходит компиляция функции `f` и сохранение адреса на созданный `PyObject` в глобальную переменную (именуем ее `compiled_func`).

```cpp
PyAPI_FUNC(PyObject *) Py_CompileStringExFlags(
    const char *str,
    const char *filename,       /* decoded from the filesystem encoding */
    int start,
    PyCompilerFlags *flags,
    int optimize);
```

Согласно структуре `struct PyModuleDef` находим нужный список функций (именуем их `Spell_function` и `Dispell_function`), определенных в текущем модуле:
![alt text](assets\image-2.png)

Анализ функции `Spell_function` или `Spell`
---

В данной функции как раз и проиcходит hook функции сравнения int объектов:
![alt text](assets\image-3.png)

Прототип `PyLong_FromLong`:
```cpp
 PyAPI_FUNC(PyObject *) PyLong_FromLong(long);
```

На основе указателя возвращенного объекта берется структура базового типа int и перехватывается вызов сравнения.

```cpp
PyObject *pyobj = PyLong_FromLong(-1); 
void *tp_richcompare = pyobj->ob_type->tp_richcompare;
*pyobj->ob_type->tp_richcompare = hook_tp_richcompare;
```
Некоторые структуры, использованные для высчитывания оффсетов:
```cpp
// longobject.h
typedef struct _longobject PyLongObject;

// longintrepr.h
struct _longobject {
    PyObject_VAR_HEAD
    digit ob_digit[1];
};

// object.h
typedef struct _typeobject PyTypeObject;

typedef struct _object {
    _PyObject_HEAD_EXTRA
    Py_ssize_t ob_refcnt;
    PyTypeObject *ob_type; // 0x8
} PyObject;

typedef struct {
    PyObject ob_base;
    Py_ssize_t ob_size; /* Number of items in variable part */
} PyVarObject;

#define PyObject_VAR_HEAD      PyVarObject ob_base;

// cpython/object.h
struct _typeobject {
    PyObject_VAR_HEAD
    const char *tp_name;
    // ...
    richcmpfunc tp_richcompare; // 0xC8
    // ...
}
```

Анализ функции `hook_tp_richcompare`
---

Прототип самой функции сравнения выглядит следующим образом:
```cpp
PyObject *tp_richcompare(PyObject *self, PyObject *other, int op);
```
Соответственно аргументы hook функции будут следующие:
```cpp
void *__fastcall hook_tp_richcompare(void *self, void *other, unsigned int op)
```

`self` и `other` - числа, которые сравниваются.

Тип `PyObject` - это лишь общая структура для всех объектов в `CPython`. В зависимости от контекста работы кода такие объекты `PyObject` преобразуются в более конкретные типы, в частности, для представления чисел используется тип `PyLongObject`. Таким образом, наиболее точный прототип функции `hook_tp_richcompare` можно задать следующим образом:

```cpp
void *__fastcall hook_tp_richcompare(PyLongObject *obj_UserNum, PyLongObject *obj_InsNum, unsigned int op)
```

Зададим header файл с `PyLongObject` и загрузим в IDA:

```cpp
#define _PyObject_HEAD_EXTRA

typedef uint32_t digit;
typedef ssize_t Py_ssize_t;
typedef void PyTypeObject;

typedef struct _object {
    _PyObject_HEAD_EXTRA
    Py_ssize_t ob_refcnt;
    PyTypeObject *ob_type;
} PyObject;

typedef struct _pyvarobject {
    PyObject ob_base;
    Py_ssize_t ob_size; /* Number of items in variable part */
} PyVarObject;

#define PyObject_VAR_HEAD      PyVarObject ob_base;

struct _longobject {
    PyObject_VAR_HEAD
    digit ob_digit[1];
};

typedef struct _longobject PyLongObject;
```

Таким образом декомпилированный код станет более читаемым:

![alt text](assets\image-4.png)

Общий алгоритм hook функции можно охарактеризовать следующим образом:

1. Вызов оригинальной функции сравнения и сохранение ее результата.
2. Если операция сравнения является `==`, то выполняется виртуальная машина с 5тью операциями. Номер инструкции и операнды виртуальной машины извлекаются из обоих сравниваемых чисел (`serial_NUM` и `ins_NUM`), передаваемых в функцию `tp_richcompare`.
3. В зависимости от результатов выполняемых инструкции VM происходит расшифровка (`XOR`) флага длиной `0x32`, где в качестве ключа, используются байты `serial_NUM`

![alt text](assets\image-5.png)

Каждая инструкция VM это фактически последовательность байткодов python. Байткоды инструкций VM пишутся в уже готовый объект `PyCodeObject`, который извлекается из ранее сформированного объекта, созданного при инициализации модуля (вспоминаем про вызов `Py_CompileStringExFlags` и сохранение результата в `compiled_func`).

![alt text](assets\image-7.png)

Задав тип `PyCodeObject` для `pycode_object`, получим наиболее читаемый вариант псевдокода:

![alt text](assets\image-8.png)

Как видно, в данном фрагменте перезаписывается адрес `pycode_object->co_code`, который должен указывать на объект типа `PyBytesObject`, тем самым происходит подмена байткода. Таким образом по адресу `&bytes_obj` должен располагаться объект `PyBytesObject` и можем его задать:

![alt text](assets\image-9.png)

Таким образом, видно что в функцию `sub_180001660` передается адрес, где будут располагаться байты байткода, и еще три числовых аргумента, назначение которых будет понятно, исходя из её анализа.

Кратко данную функцию можно разбить на три части:

![](assets\image-10.png)

1. Поиск места, откуда будет браться байткод.
2. Считывание байтов и запись их в подготовленную область для байткода. С какого оффсета считывать байты и на какой оффсет записывать, определяются как раз тремя последними переданными аргументами.
3. Выставление корректного размера для объекта `PyBytesObject`.

Таким образом можно выделить 5 возможных последовательностьей байткод:
```python
# XOR
64 00 64 01 40 00 64 02 41 00 64 03 6b 02 53 00
              0 LOAD_CONST               0 (consts[0])
              2 LOAD_CONST               1 (consts[1])
              4 BINARY_AND
              6 LOAD_CONST               2 (consts[2])
              8 BINARY_XOR
             10 LOAD_CONST               3 (consts[3]))
             12 COMPARE_OP               2 (==)
             14 RETURN_VALUE


# ADD
64 00 64 01 40 00 64 02 17 00 64 01 40 00 64 03 6b 02 53 00
              0 LOAD_CONST               0 (consts[0])
              2 LOAD_CONST               1 (consts[1])
              4 BINARY_AND
              6 LOAD_CONST               2 (consts[2]))
              8 BINARY_ADD
             10 LOAD_CONST               1 (consts[1])
             12 BINARY_AND
             14 LOAD_CONST               3 (consts[3])
             16 COMPARE_OP               2 (==)
             18 RETURN_VALUE

# SUB
64 00 64 01 40 00 64 02 18 00 64 01 40 00 64 03 6b 02 53 00
              0 LOAD_CONST               0 (consts[0])
              2 LOAD_CONST               1 (consts[1])
              4 BINARY_AND
              6 LOAD_CONST               2 (consts[2])
              8 BINARY_SUBTRACT
             10 LOAD_CONST               1 (consts[1])
             12 BINARY_AND
             14 LOAD_CONST               3 (consts[3])
             16 COMPARE_OP               2 (==)
             18 RETURN_VALUE


# MUL
64 00 64 01 40 00 64 02 14 00 64 01 40 00 64 03 6b 02 53 00
              0 LOAD_CONST                0 (consts[0])
              2 LOAD_CONST               1 (consts[1])
              4 BINARY_AND
              6 LOAD_CONST               2 (consts[2])
              8 BINARY_MULTIPLY
             10 LOAD_CONST               1 (consts[1])
             12 BINARY_AND
             14 LOAD_CONST               3 (consts[3])
             16 COMPARE_OP               2 (==)
             18 RETURN_VALUE
# DIV
64 00 64 01 40 00 64 02 1a 00 64 01 40 00 64 03 6b 02 53 00
              0 LOAD_CONST               0 (consts[0])
              2 LOAD_CONST               1 (consts[1])
              4 BINARY_AND
              6 LOAD_CONST               2 (consts[2])
              8 BINARY_FLOOR_DIVIDE
             10 LOAD_CONST               1 (consts[1])
             12 BINARY_AND
             14 LOAD_CONST               3 (consts[3])
             16 COMPARE_OP               2 (==)
             18 RETURN_VALUE
```

Или в python интерпретации:
```python
def XOR():
	return ((consts[0] & consts[1]) ^ consts[2]) == consts[3]

def ADD():
	return (((consts[0] & consts[1]) + consts[2]) & consts[1]) == consts[3]

def SUB():
	return (((consts[0] & consts[1]) - consts[2]) & consts[1]) == consts[3]

def MUL():
	return (((consts[0] & consts[1]) * consts[2]) & consts[1]) == consts[3]

def DIV():
	return (((consts[0] & consts[1]) // consts[2]) & consts[1]) == consts[3]
```

После перезаписанного байткода в `pycode_object`, далее перезаписываются константы:

![alt text](assets\image-11.png)
Порядок записи констант зависит от числа в старшем полубайте DWORD-а `ins`.

После того, как `pycode_object` сформирован, он вызывается

![alt text](assets\image-12.png)

И результат проверяется на то, что результат не ложный (PyFalse_Type) (в функции `sub_180001080`). Если `result_obj` стал true объектом (в cpython `True` объект - это фактически объект типа `PyLongObject` со значением 1 в поле `digit`), то байта флага ксорится.

Стоит отметить, что если передаваемый DWORD `ins` равен `0xDEADDEAD`, то происходит возвращение строки флага:

![alt text](assets\image-13.png)

![alt text](assets\image-14.png)

Таким образом, проанализировав при каких значения старшего полубайта `ins` формируется тот или иной порядок констант, можно сформировать следующий скрипт для генерации серийного номера:

```python
import struct

def XORgen(ins): # 0x2
	user_input = [0x0, 0x0, 0x0, 0x0]
	order = ins[-1] & 0xF0
	num1 = ins[-2]

	for idx in range(4):
		if order == 0x10:
			user_input[idx] = ins[idx] ^ num1
		elif order == 0x20:
			user_input[idx] = ins[idx] ^ num1
		elif order == 0x30:
			pass
		else:
			user_input[idx] = ins[idx] ^ num1
	return user_input


def ADDgen(ins): # 0x3
	user_input = [0x0, 0x0, 0x0, 0x0]
	order = ins[-1] & 0xF0
	num1 = ins[-2]

	for idx in range(4):
		if order == 0x10:
			user_input[idx] = (num1 - ins[idx]) & 0xFF
		elif order == 0x20:
			user_input[idx] = (ins[idx] - num1) & 0xFF
		elif order == 0x30:
			pass
		else:
			user_input[idx] = (ins[idx] - num1) & 0xFF
	return user_input

def SUBgen(ins): # 0x5
	user_input = [0x0, 0x0, 0x0, 0x0]
	order = ins[-1] & 0xF0
	num1 = ins[-2] 

	for idx in range(4):
		if order == 0x10:
			user_input[idx] = (ins[idx] + num1) & 0xFF
		elif order == 0x20:
			user_input[idx] = (num1 - ins[idx]) & 0xFF
		elif order == 0x30:
			pass
		else:
			user_input[idx] = (ins[idx] + num1) & 0xFF
	return user_input

def MULgen(ins): # 0x7
	user_input = [0x0, 0x0, 0x0, 0x0]
	order = ins[-1] & 0xF0
	num1 = ins[-2]

	for idx in range(4):
		if order == 0x10:
			pass
		elif order == 0x20:
			pass
		elif order == 0x30:
			user_input[idx] = (num1 * ins[idx]) & 0xFF
		else:
			pass
	return user_input

ins = [0xd2ff820b, 0x37339d0a, 0x373f2dcf, 0xd539fdd6, 0x15bcf78b, 0x3726c467, 0x37694359, 0xd23652c1, 0x15f9585a, 0x153df12f, 0x15fd2ae5, 0x23c1bbf9, 0x150edcfb, 0x376621d7, 0x220d4767, 0x2314d933, 0x230b8111, 0xd35fc81e, 0x138dfa5b, 0x12e3622b, 0x37886c57, 0x3737bdbe, 0xd2142d76, 0x37230e39, 0x1361d5d8, 0x37de6079, 0x22085d4d, 0xd5050afb, 0x373d5935, 0x37b34ed7, 0x2553d571, 0x120359ea, 0x2587fc6c, 0xd256177a, 0x13c75429, 0x259ff74e, 0xd2fe6926, 0x1272e06c, 0x378858c7, 0x23ef48a0, 0xd230103a, 0x121068c5, 0x37919294, 0x22ef7b6a, 0x23a4c5ee, 0x375bda25, 0x1211453a, 0x237158ec, 0x1578a82a]

ops = {0x2: XORgen, 0x3: ADDgen, 0x5: SUBgen, 0x7: MULgen}
for i in ins:
	op = (i >> 24) & 0x0F
	func = ops[op]
	user_input = func(struct.pack("I", i))
	user_input = struct.pack("BBBB", *user_input)
	
	print(user_input.hex(), end="")
print()
```
Таким образом вводимый серийный номер при данном `ins` должен быть следующим:
`f47d002dfe4729f5f11381890f36720e47b378d14a18a42a817b118ff76400e45351f20e6c2e7a52e227fa1238fa006209ea1c23aa26a4ea6a4a002f1fc5000f06760018bf6900743293007ac88100f138604038d29bd1d1623900c6cbeac985898c004eee4084b24555002a000f0adaa135891b558a2975e27e002ee95a00111b8b00622c4100849e7300b451a8007ad897002c1e920060b8c04038b15900340a2000e2d5780002d4b22127859400cd4a21007f277e598d2b5400037be700b2a220f08d`

![alt text](assets\image-15.png)

FLAG
===
```
rdg{f3ea59c0_T4k3_Y0ur_r3w4rd_PY0b1ect_N1nja_17c26f69}
```