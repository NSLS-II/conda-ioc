import logging
import time

from pypvserver import (PypvServer, logger as server_logger)

import pseudomotors


def loop():
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print('Done')


def main():
    server = PypvServer(prefix='XF:03IDC-ES')
    info = pseudomotors.setup(server)

    print('')
    print('* PVs:')
    for pv in info.get('pvs', []):
        print('\t', pv)

    print('')
    print('* Positioners:')
    for positioner in info.get('positioners', []):
        print('\t', positioner)

    print('')
    print('* PyPV motors:')
    for motor in info.get('pypv_motors', []):
        print('\t', motor)

    loop()


if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    logger.setLevel(logging.DEBUG)
    server_logger.setLevel(logging.DEBUG)
    logging.basicConfig()
    main()
