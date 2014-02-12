#!/usr/bin/env python
# coding=utf-8
import sys, traceback, subprocess
from flask.ext.script import Shell, Manager
from bl.helpers import IceAdapters

import Ice
from app import app


manager = Manager(app)


@manager.command
def clean_pyc():
    """Removes all *.pyc files from the project folder"""
    clean_command = "find . -name *.pyc -delete".split()
    subprocess.call(clean_command)


@manager.command
def ice_server():
    status = 0
    ic = None

    try:
        ic = Ice.initialize(sys.argv)
        for adapter_point in IceAdapters:
            conn_params = IceAdapters[adapter_point]['conn']
            adapter = ic.createObjectAdapterWithEndpoints(
                adapter_point, conn_params
            )
            for meth in IceAdapters[adapter_point]['reg']:
                cls_, cls_str = meth
                adapter.add(cls_(), ic.stringToIdentity(cls_str))

            adapter.activate()
            ic.waitForShutdown()
    except:
        traceback.print_exc()
        status = 1

    if ic:
        try:
            ic.destroy()
        except:
            traceback.print_exc()
            status = 1

    sys.exit(status)


manager.add_command('shell', Shell(make_context=lambda:{'app': app}))


if __name__ == '__main__':
    manager.run()
