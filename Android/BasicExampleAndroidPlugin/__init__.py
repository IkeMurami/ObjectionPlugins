__description__ = "Kotlin Plugin"

import argparse
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
                    'exec': self.frida_hook,
                }
            }
        }

        super().__init__(__file__, ns, implementation)

        self.inject()

    def argparser(self):
        parser = argparse.ArgumentParser(description='Argparser for command')

        parser.add_argument('-t', '--test', help='It is a some arg', required=False)

        return parser

    def frida_hook(self, args: list):
        # args = ['-t', '123', '-s', ...]
        # How work with args
        args = self.argparser().parse_args(args)
        print(args.test)

        # Call RPC function
        res = self.api.fridafunction('put some arguments')

        print(f'Result: {res}')


namespace = 'androidExample'
plugin = KotlinPlugin