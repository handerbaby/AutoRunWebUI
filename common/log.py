import logging
import os
from logging.handlers import TimedRotatingFileHandler
from common.config import Config
from common.filedir import LOGDIR

class Handlogging():

    def emplorlog(self):
        conf = Config()
        formatter = logging.Formatter("%(asctime)s - %(name)s-%(levelname)s %(message)s")

        mylog = logging.getLogger('Admin')
        mylog.setLevel(conf.get('Log', 'level'))

        sh = logging.StreamHandler()
        sh.setLevel(conf.get('Log', 'level'))
        sh.setFormatter(formatter)
        mylog.addHandler(sh)

        log_path = os.path.join(LOGDIR, 'test')
        fh = TimedRotatingFileHandler(filename=log_path, when='D', backupCount=15, encoding='utf-8')
        fh.suffix = '%T-%m-%d.log'
        fh.setLevel(conf.get('Log', 'level'))
        fh.setFormatter(formatter)
        mylog.addHandler(fh)
        return mylog