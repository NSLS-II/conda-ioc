import math
import logging

from ophyd import (PseudoSingle, PseudoPositioner,
                   EpicsSignal, EpicsMotor,
                   Component as Cpt)

from ophyd.pseudopos import (real_position_argument,
                             pseudo_position_argument)


class FineSampleLabX(PseudoPositioner):
    # pseudo axes
    theta = Cpt(PseudoSingle)

    # real axes
    zpssx = Cpt(EpicsMotor, '{Ppmac:1-zpssx}Mtr')
    zpssz = Cpt(EpicsMotor, '{Ppmac:1-zpssz}Mtr')

    # configuration settings
    theta0 = Cpt(EpicsSignal, '{PseudoPos-ZP}theta0')

    def __init__(self, prefix, **kwargs):
        super().__init__(prefix, **kwargs)

        # if theta0 changes, update the pseudo position
        self.theta0.subscribe(self.parameter_updated)

    def parameter_updated(self, value=None, **kwargs):
        self._update_position()

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        theta0 = self.theta0.get()
        angle = math.radians(pseudo_pos.theta + theta0)
        return self.RealPosition(zpssx=math.cos(angle),
                                 zpssz=-math.sin(angle),
                                 )

    @real_position_argument
    def inverse(self, position):
        theta0 = self.theta0.get()
        theta = math.degrees(math.acos(position.zpssx))
        return self.PseudoPosition(theta=theta - theta0)


def setup(server):
    from pypvserver import (PyPV, PypvMotor)

    py_theta0 = PyPV('{PseudoPos-ZP}theta0', 0., server=server)
    zpssx_lab = FineSampleLabX('XF:03IDC-ES')

    motor_zpssx_lab = PypvMotor('{PseudoPos-ZP}zpssx_lab', zpssx_lab.theta,
                                server=server)

    return {'pvs': [py_theta0],
            'positioners': [zpssx_lab, ],
            'pypv_motors': [motor_zpssx_lab, ]
            }
