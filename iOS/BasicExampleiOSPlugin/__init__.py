__description__ = "iOS Swift Plugin Test"

import os
from objection.utils.plugin import Plugin


class SwiftPlugin(Plugin):
    """ Swift Plugin """

    def __init__(self, ns):
        """
        
        """

        self.script_path = os.path.join(os.path.dirname(__file__), "script.js")

        implementation = {
            'meta': 'Swift Plugin',
            'commands': {
                'dump': {
                    'meta': 'Test some functions',
                    'exec': self.dump
                }
            }
        }

        super().__init__(__file__, ns, implementation)

        self.inject()

    def dump(self, args: list):
        # print(self.script_path)
        self.api.test()


namespace = 'ios'
plugin = SwiftPlugin