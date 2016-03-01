import logging
import time

# import ophyd
from pypvserver import (PypvServer, PyPV,
                        logger as server_logger)


logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
server_logger.setLevel(logging.DEBUG)
logging.basicConfig()


server = PypvServer(prefix='test_prefix:')
logger.info('Creating PV "pv1", a floating-point type')
python_pv = PyPV('pv1', 123.0, server=server)

# full_pvname includes the server prefix
pvname = python_pv.full_pvname
logger.info('... which is %s including the server prefix', pvname)

time.sleep(0.1)

for value in range(10):
    logger.info('Updating the value on the server-side to: %s', value)
    python_pv.value = value
    time.sleep(0.05)

logger.info('Done')

try:
    while True:
        time.sleep(1.0)
except KeyboardInterrupt:
    print('Done')
