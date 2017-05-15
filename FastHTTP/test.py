import os
import yaml
import logging
import logging.config


def setup_logging(
    default_path='logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    value = os.getenv(env_key, None)
    if value is None:
        path = default_path
    else:
        path = value

    if os.path.exists(path) and os.path.isfile(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
        

setup_logging()

logger = logging.getLogger('my_module')
logging.info('ads')
logger.infoecd('this i awesom')