
function prints(s) {
    console.log(s);
}

function nsstring(s) {
    const { NSString } = ObjC.classes
    return NSString.stringWithString_(s)
}

function GetModules() {
    let modules = Process.enumerateModules();
    modules.forEach(function(item) {
        if (!item.path.includes("/System/Library") && !item.path.includes("/usr/lib")) {

            // prints(`Name: ${item.name}; Path: ${item.path}`);
        }
    });

    return modules;
}



function GetModule(name) {
    let modules = GetModules();

    return modules.filter(function(item) {
        return item.name == name
    })[0];
}

function ModuleExports(module) {

    let exports = module.enumerateExports();
    let funcs = exports.filter(function(item) {
        return item.type === 'function'
    });
    let vars = exports.filter(function(item) {
        return item.type === 'variable'
    });

    return {
        'funcs': funcs,
        'vars': vars
    }
}

function VarsTest(vars) {
    vars.forEach(function(item) {
        // prints(`Name: ${item.name}`);
    })
}

function GetVariableByName(vars, name) {
    return vars.filter(function(item) {
        return item.name === name
    })[0];
}

rpc.exports = {
    testSwift: function() {
        console.log("[+] Swift plugin started");
        if (Swift.available) {
            try {
                console.log("[+] Swift Runtime Available");

                let modules = GetModules();
                let messProtoModule = GetModule("MessProto");
                let exports = ModuleExports(messProtoModule);

                let verifyCodeRequestInit = GetVariableByName(exports.vars, '$s9MessProto0B17VerifyCodeRequestVACycfC');
                // prints(`Name: ${verifyCodeRequestInit.name}, Address: ${verifyCodeRequestInit.address}`)

                let obj = new Swift.Object(verifyCodeRequestInit.address);
            }
            catch(err) {
                console.log("[!] Exception: " + err.message);
            }
        }
        else {
            console.log("Swift Runtime is not available!");
        }
    },
    test: function() {
        console.log("[+] ObjC plugin started")
        if (ObjC.available) {
            try {
                console.log("[+] ObjC Runtime Available");
                
                
                let grpcClient = GetModule("GRPCClient")
                let exports = ModuleExports(grpcClient)
                prints(`${exports.funcs.length} and ${exports.vars.length}`)
                exports.vars.forEach(function(item) {
                    if (item.name.includes("CallOptions")) {
                        // prints(`${item.name} ${item.address}`)
                    }
                })


                let target = ObjC.classes.GRPCMutableCallOptions
                Interceptor.attach(target['- init'].implementation, {
                    onEnter: function (args) {
                        prints(`CJABJHCBD`)
                    },
                    onLeave: function (retval) {
                        try {
                            let grpcMutableCallOptions = new ObjC.Object(retval)
                            prints(`Retval: ${grpcMutableCallOptions}`)
                            prints(`Do: ${grpcMutableCallOptions.PEMRootCertificates()}`)
                            // grpcMutableCallOptions.setRetryEnabled
                            prints(`???: ${grpcMutableCallOptions.RetryEnabled}`)
                            grpcMutableCallOptions.setPEMRootCertificates = nsstring("");
                            prints(`posle: ${grpcMutableCallOptions.PEMRootCertificates}`)
                            retval = grpcMutableCallOptions
                        }
                        catch(err1) {
                            prints(err1.message)
                        }
                        prints(`kdvjhshjdkdkfjv`)
                    }
                })

            }
            catch(err) {
                console.log("[!] Exception: " + err.message);
            }
        }
        else {
            console.log("ObjC Runtime is not available!");
        }
    }
}
