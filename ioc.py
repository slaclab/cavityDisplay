#!/usr/bin/env python3
from textwrap import dedent

from caproto.server import PVGroup, ioc_arg_parser, pvproperty, run


class SimpleIOC(PVGroup):
    """
    An IOC with three uncoupled read/writable PVs

    Scalar PVs
    ----------
    A (int)
    B (float)

    Vectors PVs
    -----------
    C (vector of int)
    """
    AO011 = pvproperty(value=1, doc='An integer')
    AO012 = pvproperty(value=1, doc='An integer')
    AO013 = pvproperty(value=1, doc='An integer')
    AO014 = pvproperty(value=1, doc='An integer')
    AO015 = pvproperty(value=1, doc='An integer')
    AO016 = pvproperty(value=1, doc='An integer')
    AO017 = pvproperty(value=1, doc='An integer')
    AO018 = pvproperty(value=1, doc='An integer')
    AO019 = pvproperty(value=1, doc='An integer')
    AO020 = pvproperty(value=1, doc='An integer')
    AO021 = pvproperty(value=1, doc='An integer')
    AO022 = pvproperty(value=1, doc='An integer')


if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='SIOC:SYS0:ML07:',
        desc=dedent(SimpleIOC.__doc__))
    ioc = SimpleIOC(**ioc_options)
    run(ioc.pvdb, **run_options)