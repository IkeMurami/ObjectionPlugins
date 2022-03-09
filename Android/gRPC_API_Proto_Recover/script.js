
function prints(s) {
    console.log(s)
}


class JavaIntrospector {

    ClassObject(klassName) {
        const klass = Java.use(klassName)
        return klass.$new()
    }

    Methods(klassName, toLowerCase=false, methodTemplate='*') {
        // TODO: Как себя будет вести функция на вложенных классах?
        // const klass = Java.use(klassName)
        const loaders = Java.enumerateMethods(`${klassName}!${methodTemplate}*/isu`)  // Include method signatures (s) and User-defined classes only, ignoring system classes. (u) and case sensitive (i)
        let methods = new Map()
        
        loaders.forEach(function(loader) {
            loader.classes.forEach(function(klass){
                klass.methods.forEach(function(method) {
                    let key = method.split(': ')[0]
                                    .split('(')[0]
                    // prints(method)
                    const args = method.split(': ')[0]
                                       .split('(')[1]
                                       .split(')')[0]
                    const value = method.split(': ')[1]

                    if (toLowerCase) {
                        key = key.toLowerCase()
                    }

                    methods.set(key, {typeOfArgs: args, typeOfReturn: value})
                })
            })
        })

        return methods
    }

    Fields(klassName) {
        try{
            const klass = Java.use(klassName)

            return Object.getOwnPropertyNames(klass)
        }
        catch {
        }
        return []
    }

    GetPropertyType(MethodsOfClassList, PropertyName) {

        const stringConverter = new StringConverter()

        const getter = stringConverter.GetPropertyGetterName(PropertyName)

        const oneOfAttrs = [
            true,  // for reduce
            getter,
            `${getter}Case`
        ]

        const repeatedAttrs = [
            true,  // for reduce
            getter,
            `${getter}Bytes`,
            `${getter}Count`,
            `${getter}List`
        ]

        const mapAttrs = [
            true,  // for reduce
            getter,
            `${getter}Count`,
            `${getter}Map`,
            `${getter}OrDefault`,
            `${getter}OrThrow`
        ]

        const attrChecker = (status, method) => {
            return status && MethodsOfClassList.has(method.toLowerCase())
        }

        const isMap = mapAttrs.reduce(attrChecker)
        const isRepeated = repeatedAttrs.reduce(attrChecker)
        const isOneOf = oneOfAttrs.reduce(attrChecker)   // TODO: oneof вообще по другому оттображается: для него нет дескриптора, его надо отыскивать по полям, что имеют тип Object

        const retValue = {
            isMap: false,
            isRepeated: false,
            isOneOf: false,
            typeFrom: undefined,
            typeTo: undefined,
            type: undefined
        }

        if (isMap || isRepeated || isOneOf) {
            if (isMap) {
                const signatureOfMethod = MethodsOfClassList.get(`${getter}OrThrow`.toLowerCase())

                retValue.isMap = true
                retValue.typeFrom = signatureOfMethod.typeOfArgs
                retValue.typeTo = signatureOfMethod.typeOfReturn
            }
            if (isRepeated) {
                const signatureOfMethod = MethodsOfClassList.get(`${getter}`.toLowerCase())
                
                retValue.isRepeated = true
                retValue.type = signatureOfMethod.typeOfReturn
            }
            if (isOneOf) {
                retValue.isOneOf = true
                // TODO
            }
        }
        else {
            const signatureOfMethod = MethodsOfClassList.get(`${getter}`.toLowerCase())
            
            retValue.type = signatureOfMethod.typeOfReturn
        }

        return retValue
    }

}


class StringConverter {
    CONST_FIELD_NUMBER = '_FIELD_NUMBER'

    UCFirst = (s) => s.charAt(0).toUpperCase() + s.slice(1)
    reducer = (prev, curr) => prev + this.UCFirst(curr.toLowerCase())

    GetPropertyName(FieldNumberName) {
        const descrName = FieldNumberName.split(this.CONST_FIELD_NUMBER)[0]
        const partDescrName = descrName
            .split('_')
            .map((item) => item.toLowerCase())
            .reduce((prev, curr) => prev + this.UCFirst(curr))
        
        return `${partDescrName}_`
    }

    GetPropertyGetterName(PropertyName) {
        // abuse_ -> getAbuse()
        const name = this
            .UCFirst(PropertyName)
            .replaceAll('_', '')
        
        return `get${name}`  
    }
}

class KotlinProtoRecover {

    CONST_BASE_CLASS_NAME = 'com.google.protobuf.GeneratedMessageLite'
    CONST_FIELD_NUMBER = '_FIELD_NUMBER'

    stringConverter = new StringConverter()
    javaIntrospector = new JavaIntrospector()

    constructor() {}

    _GenerateMessageLiteFilter(className) {
        // Проверяем, что класс имплементит специфичные для GeneratedMessageLite методы
        // Таким образом, находим все дочерние классы
        const CONST_BASE_METHODS = [true, 'getDefaultInstance', 'parseFrom', 'parser', 'newBuilder']
        const fieldsAndMethods = new JavaIntrospector().Fields(className)
        return CONST_BASE_METHODS.reduce((isContains, method) => {
            return isContains && fieldsAndMethods.includes(method)
        })
    }
    
    ProtoRecoveService(packageName) {
        const methods = this.javaIntrospector.Fields(packageName)
        // const klass_f = Java.use('io.grpc.f').$new()
        // const klass_e = Java.use('io.grpc.e').$new()
        // const klass = Java.use(packageName).$new(klass_f, klass_e)
        // prints(`klass.a = ${klass.a}`)
        // prints(`klass._a = ${klass._a}`)
        methods.forEach((item) => {
            prints(`${packageName}: ${item}`)
        })
    }

    ProtoRecoveClass(klassName) {
        // prints(`Start Recover`)
        const klass = Java.use(klassName)

        const klassObj = this.javaIntrospector.ClassObject(klassName)
        const fields = this.javaIntrospector.Fields(klassName)
        const methods = this.javaIntrospector.Methods(klassName, true)
        
        // prints(`Init values`)

        let obj = {
            name: klassName,
            messages: [],
            fields: []
        }

        fields.filter(function(item) {
            return item.includes('_FIELD_NUMBER')
        }).forEach(function(FieldNumberName) {
            const property_name = new StringConverter().GetPropertyName(FieldNumberName)
            const typeOfProperty = new JavaIntrospector().GetPropertyType(methods, property_name)
            
            // return
            const FieldNumberValue = klassObj[FieldNumberName].value
            // prints(`${typeOfProperty} ${property_name} = ${FieldNumberValue}`)

            obj.fields.push({
                id: FieldNumberValue,
                name: property_name,
                type: typeOfProperty
            })
        })

        return obj
    }

}

rpc.exports = {
    test: function(classes) {
        let ret = undefined
        prints("[+] Kotlin plugin started")
        Java.perform(function() {
            if (Java.available) {
                const messages = []
                try {
                    prints("[+] Java Runtime Available")
                    prints(`Count: ${classes.length}`)
                    
                    // const ClassName = 'my.example.app.SomeClass$SomeSubclass'
                    const recover = new KotlinProtoRecover()
                    
                    classes.forEach(function(className) {
                        // prints(`${className}`)
                        const msg = recover.ProtoRecoveClass(className)
                        messages.push(msg)
                    })
                    

                    // recover.ProtoRecoveService('my.example.app.k')
                    // recover.ProtoRecoveService('my.example.app.k$a')

                    prints('END...')
                    // recover.ProtoRecove(ClassName)
                    // recover.ProtoRecove()
                    /* 
                    Переопределить нужный метод у io.grpc.e (пока не в динамике), чтобы возвращался объект
                    */

                    ret = messages
                }
                catch(err) {
                    console.log("[!] Exception: " + err.message)
                }
            }
            else {
                console.log("Java Runtime is not available!")
            }            
        });
        
        return ret
    }
}

