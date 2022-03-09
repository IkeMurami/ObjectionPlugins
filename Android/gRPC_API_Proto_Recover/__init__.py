__description__ = "Kotlin Swift Aitu Test"

import os
import pathlib
from objection.utils.plugin import Plugin

classes = [
    'com.google.api.Advice',
    'com.google.api.AuthProvider',
    'com.google.api.AuthRequirement',
    'com.google.api.Authentication',
    'com.google.api.AuthenticationRule',
    'com.google.api.Backend',
    'com.google.api.BackendRule',
    'com.google.api.Billing$BillingDestination',
    'com.google.api.Billing',
    'com.google.api.ConfigChange',
    'com.google.api.Context',
    'com.google.api.ContextRule',
    'com.google.api.Control',
    'com.google.api.CustomHttpPattern',
    'com.google.api.Distribution$BucketOptions$Explicit',
    'com.google.api.Distribution$BucketOptions$Exponential',
    'com.google.api.Distribution$BucketOptions$Linear',
    'com.google.api.Distribution$BucketOptions',
    'com.google.api.Distribution$Exemplar',
    'com.google.api.Distribution$Range',
    'com.google.api.Distribution',
    'com.google.api.Documentation',
    'com.google.api.DocumentationRule',
    'com.google.api.Endpoint',
    'com.google.api.Http',
    'com.google.api.HttpBody',
    'com.google.api.HttpRule',
    'com.google.api.JwtLocation',
    'com.google.api.LabelDescriptor',
    'com.google.api.LogDescriptor',
    'com.google.api.Logging$LoggingDestination',
    'com.google.api.Logging',
    'com.google.api.Metric',
    'com.google.api.MetricDescriptor$MetricDescriptorMetadata',
    'com.google.api.MetricDescriptor',
    'com.google.api.MetricRule',
    'com.google.api.MonitoredResource',
    'com.google.api.MonitoredResourceDescriptor',
    'com.google.api.MonitoredResourceMetadata',
    'com.google.api.Monitoring$MonitoringDestination',
    'com.google.api.Monitoring',
    'com.google.api.OAuthRequirements',
    'com.google.api.Page',
    'com.google.api.ProjectProperties',
    'com.google.api.Property',
    'com.google.api.Quota',
    'com.google.api.QuotaLimit',
    'com.google.api.ResourceDescriptor',
    'com.google.api.ResourceReference',
    'com.google.api.Service',
    'com.google.api.SourceInfo',
    'com.google.api.SystemParameter',
    'com.google.api.SystemParameterRule',
    'com.google.api.SystemParameters',
    'com.google.api.Usage',
    'com.google.api.UsageRule',
    'com.google.cloud.audit.AuditLog',
    'com.google.cloud.audit.AuthenticationInfo',
    'com.google.cloud.audit.AuthorizationInfo',
    'com.google.cloud.audit.RequestMetadata',
    'com.google.firebase.perf.v1.AndroidApplicationInfo',
    'com.google.firebase.perf.v1.AndroidMemoryReading',
    'com.google.firebase.perf.v1.ApplicationInfo',
    'com.google.firebase.perf.v1.CpuMetricReading',
    'com.google.firebase.perf.v1.GaugeMetadata',
    'com.google.firebase.perf.v1.GaugeMetric',
    'com.google.firebase.perf.v1.NetworkConnectionInfo',
    'com.google.firebase.perf.v1.NetworkRequestMetric',
    'com.google.firebase.perf.v1.PerfMetric',
    'com.google.firebase.perf.v1.PerfSession',
    'com.google.firebase.perf.v1.TraceMetric',
    'com.google.firebase.perf.v1.TransportInfo',
    'com.google.geo.type.Viewport',
    'com.google.logging.type.HttpRequest',
    'com.google.longrunning.CancelOperationRequest',
    'com.google.longrunning.DeleteOperationRequest',
    'com.google.longrunning.GetOperationRequest',
    'com.google.longrunning.ListOperationsRequest',
    'com.google.longrunning.ListOperationsResponse',
    'com.google.longrunning.Operation',
    'com.google.longrunning.OperationInfo',
    'com.google.longrunning.WaitOperationRequest',
    'com.google.protobuf.Any',
    'com.google.protobuf.Api',
    'com.google.protobuf.BoolValue',
    'com.google.protobuf.BytesValue',
    'com.google.protobuf.DescriptorProtos$DescriptorProto$ExtensionRange',
    'com.google.protobuf.DescriptorProtos$DescriptorProto$ReservedRange',
    'com.google.protobuf.DescriptorProtos$DescriptorProto',
    'com.google.protobuf.DescriptorProtos$EnumDescriptorProto$EnumReservedRange',
    'com.google.protobuf.DescriptorProtos$EnumDescriptorProto',
    'com.google.protobuf.DescriptorProtos$EnumValueDescriptorProto',
    'com.google.protobuf.DescriptorProtos$FieldDescriptorProto',
    'com.google.protobuf.DescriptorProtos$FileDescriptorProto',
    'com.google.protobuf.DescriptorProtos$FileDescriptorSet',
    'com.google.protobuf.DescriptorProtos$GeneratedCodeInfo$Annotation',
    'com.google.protobuf.DescriptorProtos$GeneratedCodeInfo',
    'com.google.protobuf.DescriptorProtos$MethodDescriptorProto',
    'com.google.protobuf.DescriptorProtos$OneofDescriptorProto',
    'com.google.protobuf.DescriptorProtos$ServiceDescriptorProto',
    'com.google.protobuf.DescriptorProtos$SourceCodeInfo$Location',
    'com.google.protobuf.DescriptorProtos$SourceCodeInfo',
    'com.google.protobuf.DescriptorProtos$UninterpretedOption$NamePart',
    'com.google.protobuf.DescriptorProtos$UninterpretedOption',
    'com.google.protobuf.DoubleValue',
    'com.google.protobuf.Duration',
    'com.google.protobuf.Empty',
    'com.google.protobuf.Enum',
    'com.google.protobuf.EnumValue',
    'com.google.protobuf.Field',
    'com.google.protobuf.FieldMask',
    'com.google.protobuf.FloatValue',
    'com.google.protobuf.GeneratedMessageLite$ExtendableMessage',
    'com.google.protobuf.Int32Value',
    'com.google.protobuf.Int64Value',
    'com.google.protobuf.ListValue',
    'com.google.protobuf.Method',
    'com.google.protobuf.Mixin',
    'com.google.protobuf.Option',
    'com.google.protobuf.SourceContext',
    'com.google.protobuf.StringValue',
    'com.google.protobuf.Struct',
    'com.google.protobuf.Timestamp',
    'com.google.protobuf.Type',
    'com.google.protobuf.UInt32Value',
    'com.google.protobuf.UInt64Value',
    'com.google.protobuf.Value',
    'com.google.rpc.BadRequest$FieldViolation',
    'com.google.rpc.BadRequest',
    'com.google.rpc.DebugInfo',
    'com.google.rpc.ErrorInfo',
    'com.google.rpc.Help$Link',
    'com.google.rpc.Help',
    'com.google.rpc.LocalizedMessage',
    'com.google.rpc.PreconditionFailure$Violation',
    'com.google.rpc.PreconditionFailure',
    'com.google.rpc.QuotaFailure$Violation',
    'com.google.rpc.QuotaFailure',
    'com.google.rpc.RequestInfo',
    'com.google.rpc.ResourceInfo',
    'com.google.rpc.RetryInfo',
    'com.google.rpc.Status',
    'com.google.rpc.context.AttributeContext$Api',
    'com.google.rpc.context.AttributeContext$Auth',
    'com.google.rpc.context.AttributeContext$Peer',
    'com.google.rpc.context.AttributeContext$Request',
    'com.google.rpc.context.AttributeContext$Resource',
    'com.google.rpc.context.AttributeContext$Response',
    'com.google.rpc.context.AttributeContext',
    'com.google.type.Color',
    'com.google.type.Date',
    'com.google.type.DateTime',
    'com.google.type.Expr',
    'com.google.type.Fraction',
    'com.google.type.LatLng',
    'com.google.type.Money',
    'com.google.type.PostalAddress',
    'com.google.type.Quaternion',
    'com.google.type.TimeOfDay',
    'com.google.type.TimeZone',

    'my.example.app.TestProtoClass'
]


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
                'dump': {
                    'meta': 'Test some functions',
                    'exec': self.dump
                }
            }
        }

        super().__init__(__file__, ns, implementation)

        self.inject()

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
        # print(self.script_path)
        # classes = ['my.example.app.SomeClass$SomeSubClassRequest']
        res = self.api.test(classes)

        self.parseResult(res, '/full/path/to/ObjectionPlugins/Android/gRPC_API_Proto_Recover/out')
        print(f'Example: {res[0]}')


namespace = 'android'
plugin = KotlinProtoRecover