__description__ = "Kotlin Swift Aitu Test"

import argparse
import os
import pathlib
from statistics import mode
from objection.utils.plugin import Plugin


"""
Есть классы, на которых фрида падает, тк для них нет конструктора без аргументов. 
Решать я это не хочу, пока не наткнусь на реальный пример полезного класса
"""
BLACK_LIST = [
    'com.google.protobuf.GeneratedMessageLite$ExtendableMessage'
]


def ReadFile(path: pathlib.Path):
    res = []
    with path.open(mode='r') as stream:
        line = stream.readline()
        while line:
            line = line.replace('\n', '')
            res.append(line)
            line = stream.readline()

    return res


class DataSaver:
    def __init__(self, base_dir_):
        self.BASE_DIR = base_dir_
        self.allPackageList = list()

    def baseNameConverter(self, nameOfType):
        baseTypes = {
            'java.lang.String': 'string',
            'java.util.Map': 'map<someType, someType>',
            'boolean': 'bool',
            'int': 'int32',
            'long': 'int64'
        }

        imports = []

        if nameOfType in baseTypes:
            nameOfType = baseTypes[nameOfType]
        elif 'com.google.protobuf' in nameOfType and 'Timestamp' not in nameOfType:
            # Заглушка, в будущем надо интоспектить и скать соотв методы у класса
            nameOfType = 'bytes'
        else:
            # kz.btsd.messenger.audiocall.Audiocall$SessionSignaling$Some   -> audiocall.Some
            packageFile = nameOfType.split('$')[0]                                          # kz.btsd.messenger.audiocall.Audiocall
            packageName = '.'.join(packageFile.split('.')[:-1])                             # kz.btsd.messenger.audiocall
            shortPackageName = packageName.split('.')[-1]                                   # audiocall
            if packageName in self.allPackageList:
                imports.append(packageFile.replace('.', '/') + '.proto')                                      # append kz.btsd.messenger.audiocall.Audiocall.proto
                nameOfType = nameOfType.replace(f'{packageName}.', '').split('$')[-1]       # kz.btsd.messenger.audiocall.Audiocall$SessionSignaling$Some -> Audiocall$SessionSignaling$Some -> Some
                nameOfType = f'{shortPackageName}.{nameOfType}'                             # audiocall.Some
                # TODO: enum correct

        return nameOfType, imports


    def nameConverter(self, message, type):
        """
        message: Message
        type: json

        return nameOfType: str, importList: List[str]
        """

        repeated = 'repeated ' if type['isRepeated'] else ''

        resImport = []

        if type['isMap']:
            fromName, imports = self.baseNameConverter(type['typeFrom']); resImport.extend(imports)
            toName, imports = self.baseNameConverter(type['typeTo']); resImport.extend(imports)
            nameOfType = f'map<{fromName}, {toName}> '
        elif type['isOneOf']:
            # TODO: определение типов для oneof
            nameOfType = f'oneof '
        else:
            nameOfType, imports = self.baseNameConverter(type['type']); resImport.extend(imports)
    
        nameOfType = repeated + nameOfType

        # TODO: формирование списка импортов

        return nameOfType, list(set(resImport))


    def collectAllUserPackages(self, packages):
        res = []
        for path in packages:
            messages = packages[path]
            package = str(pathlib.Path(messages[0].path).parent).replace('/', '.')
            res.append(package)
        
        return res
            

    def template(self, msgs):

        # Create header
        br1, br2 = '{', '}'
        header = []
        header.append('syntax = "proto3";\n')
        package = str(pathlib.Path(msgs[0].path).parent).replace('/', '.')
        header.append(f'package {package};\n')

        body = []
        resImport = []
        
        # Collect imports and create a body for a proto-file
        for msg in msgs:
            body.append(f'message {msg.name} {br1}')
            for field in msg.fields:
                nameOfType, imports = self.nameConverter(msg, field.type); resImport.extend(imports)
                # TODO: add imports
                body.append(f'\t{nameOfType} {field.name} = {field.id};')
            body.append(f'{br2}\n')

        header.extend([f'import "{i}";' for i in list(set(resImport))])
        header.append('\n\n')
        header.extend(body)

        return '\n'.join(header)

    def save(self, packages):
        # Сохраняем все пакеты, которые определены разработчиком
        self.allPackageList = self.collectAllUserPackages(packages)

        # Для всех сообщений в каждом пакете создаем соотв директорию и сохраняем туда сообщения
        for path in packages:
            p = pathlib.Path(self.BASE_DIR).joinpath(path)
            p.parent.mkdir(exist_ok=True, parents=True)
            with p.open(mode='a') as out_stream:
                out_stream.write(self.template(packages[path]))
        ...


class Message:
    
    fields = []

    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.fields = []

    def add(self, field):
        self.fields.append(field)

    def __str__(self) -> str:
        return f'Name: {self.name}, Path: {self.path}, Fields: {self.fields}'


class MessageField:
    
    def __init__(self, id, type, name):
        self.id = id
        self.type = type
        self.name = name

    def __str__(self):
        return f'id: {self.id}, type: {self.type}, name: {self.name}'


class KotlinProtoRecover(Plugin):
    """ Kotlin Proto Recover Plugin """

    def __init__(self, ns):
        """
        
        """

        self.script_path = os.path.join(os.path.dirname(__file__), "script.js")

        implementation = {
            'meta': 'Kotlin Proto Recover Plugin',
            'commands': {
                'recover': {
                    'meta': 'Recover gRPC API',
                    'exec': self.dump
                }
            }
        }

        super().__init__(__file__, ns, implementation)

        self.inject()

    def argparser(self):
        parser = argparse.ArgumentParser(description='gRPC API recover')

        parser.add_argument('-c', '--classes', help='Classes for inspection (file path)', required=True)
        parser.add_argument('-o', '--output', default='out', help='Output directory', required=False)

        return parser

    def parseResult(self, messages, base_dir):

        
        def path(className):
            parts = className.split('$')

            return parts[0].replace('.', '/') + '.proto'

        def messageName(className):
            parts = className.split('$')

            return parts[-1]

        # Prepare objects
        res = {}
        # print(f'Stats: Count Files {len(messages)}')

        for message in messages:
            if 'com.google' in message['name']:
                continue

            filePath = path(message['name'])
            msgName = messageName(message['name'])

            msg = Message(filePath, msgName)

            if filePath not in res:
                res[filePath] = []

            # print(f'Stats: msg: {msgName}, fields: {len(message["fields"])}')
            for field in message['fields']:
                # print(field)
                msg.add(MessageField(field['id'], field['type'], field['name']))

            # print(msg)
            res[filePath].append(msg)

        # Save objects
        DataSaver(base_dir).save(res)



    def dump(self, args: list):
        parser = self.argparser()
        args = parser.parse_args(args)

        classes_path = pathlib.Path(args.classes)
        output_path = pathlib.Path(args.output)

        assert classes_path.exists(), f'File doesn\'t exist: {classes_path}'
        assert output_path.exists(), f'Directory doesn\'t exist: {output_path}'

        classes = ReadFile(classes_path)

        # Удаляем проблемные классы
        for black in BLACK_LIST:
            classes.remove(black)

        # Запускаем рекавер
        res = []
        
        res = self.api.apirecover(classes)
        
        if res:
            self.parseResult(res, str(output_path))
            print(f'Example: {res[0]}')


namespace = 'grpc-api'
plugin = KotlinProtoRecover