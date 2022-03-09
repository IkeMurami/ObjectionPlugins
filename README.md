# ObjectionPlugins
My Objection Framework plugins

# Example running a some objection plugin

```shell
#!/usr/bin/env bash

objection --gadget $1 explore -P "/full/path/to/ObjectionPlugins/Android/" -s "plugin androidExample customAction"
```

# Особенности

1. Если мы подгружаем два плагина в одном namespace, то будут работать только команды из последнего подгруженного плагина

2. RPC-функции не должны содержать в своем имени спец. символы и большие буквы. Например:

Вот так функция не подтянется:

```javascript
rpc.exports = {
    frida_function: (someInputs) => {
        // ...
    },
    fridaFunction: (someInputs) => {
        // ...
    },
}
``` 

А вот так подтянется:

```javascript
rpc.exports = {
    fridafunction: (someInputs) => {
        // ...
    }
}
```

PS: Причем это ограничение только на стороне JS. То есть в JS-скрипте — `fridafunction`, а в Python-скрипте можем обратиться к этой функции по такому имени — `fridafunction`, так и по такому — `fridaFunction`. То есть регистр в Python не важен, под капотом видно все к нижнему регистру приводится

3. Походу helpfile для плагина не написать (который бы выводил информацию через `help plugin pluginName commandName`), тк для этого надо коммитить в основной репозиторий.

helpfile хранятся здесь: `objection/console/helpfiles`  
Код, который их обрабатывает (ищет) здесь: `objection/console/repl.py`, метод: `_find_command_help`. Проблема в том, что он ищет их по относительным путям.

4. Как вызвать код (Python или JS/TS) другого плагина в Objection:

Есть глобальная переменная COMMANDS, которая содержит в себе команды (и хендлеры) всех подгруженных плагинов:

Пусть мы знаем, что в системе есть плагин `PLUGIN` с командой `COMMAND` и с какими-то аргументами. Вот так мы можем вызвать python-handler, соотв этой команде:

```python
from objection.utils.plugin import Plugin

class YourPlugin(Plugin):
    """ Your Plugin """

    # ....
    
    def my_command_handler(self, args: list):
        from objection.console.commands import COMMANDS

        OTHER_PLUGIN_NAME, OTHER_PLUGIN_COMMAND = 'someplugin', 'somecmd'
        EMPTY_ARGS = []
        
        # Get all loaded plugins (and your plugins too)
        all_loaded_plugins = COMMANDS['plugin']['commands']
        # Get OTHER_PLUGIN_NAME's commands
        loaded_plugin_commands = all_loaded_plugins[OTHER_PLUGIN_NAME]['commands']
        # Get the python handler for OTHER_PLUGIN_COMMAND-command
        command_handler = loaded_plugin_commands[OTHER_PLUGIN_COMMAND]['exec']

        # Call this handler
        print('Result:', command_handler(EMPTY_ARGS))


namespace = 'androidPl2'
plugin = YourPlugin
```

=> можем делать библиотеки на основе плагинов без коммита в основной репозиторий Objection.