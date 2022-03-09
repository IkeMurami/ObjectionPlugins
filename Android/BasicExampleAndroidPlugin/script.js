
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

}


rpc.exports = {
    fridafunction: (someInputs) => {
        let ret = undefined
        prints("[+] Plugin started")
        if (Java.available) {
            Java.perform(() => {
                try {
                    prints("[+] Java Runtime Available")
                    prints(`${someInputs}`)
                    prints('END...')
                    
                    ret = 'some return value'
                }
                catch(err) {
                    prints(`[!] Exception: ${err.message}`)
                }
            })
        }
        else {
            prints("Java Runtime is not available!")
            return null
        }
        
        return ret
    }
}