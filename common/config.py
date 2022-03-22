import os
from configparser import ConfigParser
from common.filedir import CONFIGDIR

class Config(ConfigParser):
    def __init__(self):
        self.conf_name = os.path.join(CONFIGDIR, 'base.ini')
        super().__init__()
        super().read(self.conf_name, encoding='urf-8')

    def save_data(self, section, option, value):
        super().set(section=section, option=option, value=value)
        super().write(fp=open(self.conf_name, 'w'))
