__description__ = "Kotlin Plugin"

import os
import pathlib
from objection.utils.plugin import Plugin


class KotlinPlugin(Plugin):
    """ Kotlin Plugin """

    def __init__(self, ns):

        self.script_path = os.path.join(os.path.dirname(__file__), "script.js")
        
        implementation = {
            'meta': 'Kotlin Plugin',
            'commands': {
                'customAction': {
                    'meta': 'Test some functions',
                    'exec': self.frida_hook
                }
            }
        }

        super().__init__(__file__, ns, implementation)

        self.inject()

    def frida_hook(self, args: list):
        res = self.api.frida_function('put some arguments')

        print(f'Result: {res}')


namespace = 'android'
plugin = KotlinPlugin