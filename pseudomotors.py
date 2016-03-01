import math
import logging

import ophyd
from ophyd import (PseudoSingle, PseudoPositioner,
                   EpicsSignal, EpicsMotor,
                   Component as Cpt)

from ophyd.pseudopos import (real_position_argument,
                             pseudo_position_argument)


class FineSampleLabX(PseudoPositioner):
    # pseudo axes
    zpssx_lab = Cpt(PseudoSingle)
    zpssz_lab = Cpt(PseudoSingle)

    # real axes
    zpssx = Cpt(EpicsMotor, '{Ppmac:1-zpssx}Mtr')
    zpssz = Cpt(EpicsMotor, '{Ppmac:1-zpssz}Mtr')

    # configuration settings
    theta = Cpt(EpicsSignal, '{PseudoPos-ZP}theta')

    def __init__(self, prefix, **kwargs):
        super().__init__(prefix, **kwargs)

        # if theta changes, update the pseudo position
        self.theta.subscribe(self.parameter_updated)

    def parameter_updated(self, value=None, **kwargs):
        self._update_position()

    @property
    def radian_theta(self):
        return math.radians(self.theta.get())

    @pseudo_position_argument
    def forward(self, position):
        theta = self.radian_theta
        c = math.cos(theta)
        s = math.sin(theta)

        x = c * position.zpssx_lab + s * position.zpssz_lab
        z = -s * position.zpssx_lab + c * position.zpssz_lab
        return self.RealPosition(zpssx=x, zpssz=z)

    @real_position_argument
    def inverse(self, position):
        theta = self.radian_theta
        c = math.cos(theta)
        s = math.sin(theta)
        x = c * position.zpssx - s * position.zpssz
        z = s * position.zpssx + c * position.zpssz
        return self.PseudoPosition(zpssx_lab=x, zpssz_lab=z)


def setup(server):
    from ophyd.utils.startup import setup

    logging.getLogger('ophyd.ophydobj').setLevel(logging.DEBUG)
    setup()

    from pypvserver import (PyPV, PypvMotor)

    py_theta = PyPV('{PseudoPos-ZP}theta', 0., server=server)

    zp_lab = FineSampleLabX('XF:03IDC-ES', name='zp_lab')
    zp_lab.wait_for_connection()

    zp_lab.zpssx_lab.name = 'zpssx_lab'
    zp_lab.zpssz_lab.name = 'zpssz_lab'

    motor_zpssx_lab = PypvMotor('{PseudoPos-zpssx}Mtr', zp_lab.zpssx_lab,
                                precision=3,
                                server=server)
    motor_zpssz_lab = PypvMotor('{PseudoPos-zpssz}Mtr', zp_lab.zpssz_lab,
                                precision=3,
                                server=server)

    motor_zpssx_lab._move_done()
    return {'pvs': [py_theta, ],
            'positioners': [zp_lab, ],
            'pypv_motors': [motor_zpssx_lab, motor_zpssz_lab, ],
            }
