# Usage
You should prepare the list classes what extend `com.google.protobuf.GeneratedMessageLite` (see: https://github.com/IkeMurami/PyAndroidBinarySAST)

```
$ cat /full/path/to/classes.list
...
com.google.api.AuthProvider
...
$ objection --gadget "com.example.your.app" explore -P "/full/path/to/ObjectionPlugins/Android"
com.example.your.app on (google: 8.1.0) [usb] # plugin grpc-api recover -c /full/path/to/classes.list -o /full/path/to/out/directory
```

# О gRPC API полях и Smali
Поккак восстанавливал API вручную, сделал такие замечания (в другом бинаре могут быть другие названия классов и переменных, но характер будет тот же):

```
Анализ и восстановление grpc api из java-кода:

p0.k<X> -> repeated X
k -> bytes
a1<,> -> map
p0.c -> repeated ? 
Все p0.[что-то] -> repeated basic type
```

# Специфичные методы для полей:

## repeated

```
CategoryIds -> Field -> repeated SomeType
    getCategoryIds(int) -> SomeType
    getCategoryIdsBytes
    getCategoryIdsCount
    getCategoryIdsList
```

## map

```
title -> Field -> map<SomeA, SomeB>
    getTitle() -> Map
    getTitleCount()
    getTitleMap()
    getTitleOrDefault(int, String) -> String
    getTitleOrThrow(SomeA) -> SomeB
```

## oneof

Есть особенность: oneof вообще по другому отображается: для него нет дескриптора, его надо отыскивать по полям, что имеют тип Object
```
meta -> Field -> oneof meta {
                    SomeA
                    SomeB
                 }
    meta_ -> Object 
    getMetaCase()
    mergeSomeA
    mergeSomeB
```

## enum

Только в динамике?

## services

?

## bytes

Только в динамике?

Для моего приложения имеет тип: com.google.protobuf.k

Есть методы специфичные:

isEmpty
size

# Bugs:
 
На примере класса kz.btsd.messenger.dialogs.Dialogs$Dialogs -> все поля repeated, но в итоговом proto-файле это не отображено

Каждый файл импортит сам себя

Вопрос с enum не решен

Вопрос с services не решен

Вопрос с oneof полями не решен