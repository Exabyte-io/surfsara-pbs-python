#!/usr/bin/env python
#
# $Id: setup.py 434 2005-11-04 15:02:07Z bas $
#
# set ts=4
#

"""
Based on setup.py from https://github.com/ehiggs/pbs-python
@author: Ewan Higgs
"""

import sys
import os
import glob
import subprocess
import re

from distutils.core import setup, Extension
from distutils.version import LooseVersion

SOURCE_DIR = 'src'

def pbs_config():
    return 'pbs-config'

def pbs_library_compile_line(pbs_conf):
    out, err = subprocess.Popen([pbs_conf,  '--libs'], stdout=subprocess.PIPE).communicate()
    return out.rstrip()

def pbs_library(pbs_conf):
    out, err = subprocess.Popen([pbs_conf, '--libs'], stdout=subprocess.PIPE).communicate()
    stripped_prefix = out[2:].rstrip() #'-l'
    return stripped_prefix

def pbs_library_dir(pbs_conf):
    out, err = subprocess.Popen([pbs_conf, '--libdir'], stdout=subprocess.PIPE).communicate()
    return out.rstrip()

def pbs_version(pbs_conf):
    out, err = subprocess.Popen([pbs_conf, '--version'], stdout=subprocess.PIPE).communicate()
    return out.rstrip()

def my_version():
    """Extract current version from configure.in"""
    conf_in = os.path.join(os.path.dirname(__file__), 'configure.in')
    txt = open(conf_in).read()
    # patttern is AC_INIT([pbs-python], [4.6.1])
    reg =  re.compile(r'^AC_INIT\(\[pbs-python\],\s*\[(\d+\.\d+(?:\.\d+)?)\]\)', re.M)
    found = reg.search(txt)
    if found:
        return found.group(1)
    else:
        raise Exception("Unable to determine pbs_python version from configure.in at %s" % conf_in)

if __name__ == '__main__':
    pbs_conf = pbs_config()
    PBS_LIB_COMPILE_LINE=pbs_library_compile_line(pbs_conf)
    PBS_LIB_DIR=pbs_library_dir(pbs_conf)
    PBS_LIBS = pbs_library(pbs_conf)

    PBS_VERSION = pbs_version(pbs_conf)
    VERSION = my_version()

    try:
        os.unlink('src/pbs.py')
    except OSError:
        pass

    if LooseVersion(PBS_VERSION) >= LooseVersion('5.0'):
        TORQUE_VERSION='TORQUE_5'
        SOURCE_FILE='src/5.x/pbs_wrap.cxx'
        PBS_PYTHON_INCLUDE_DIR = 'src/5.x'

        if not os.path.exists(os.path.join(PBS_PYTHON_INCLUDE_DIR,'log.h')):
            print 'Failed to find log.h in include dir %s. (Set include dir via PBS_PYTHON_INCLUDEDIR variable)'%inc
            sys.exit(2)

        for fn in glob.glob('*.h'):
            os.remove(fn)

        os.symlink('5.x/pbs.py', 'src/pbs.py')

    elif LooseVersion(PBS_VERSION) >= LooseVersion('4.2'):
        TORQUE_VERSION='TORQUE_4'
        SOURCE_FILE='src/C++/pbs_wrap.cxx'
        PBS_PYTHON_INCLUDE_DIR = 'src/C++'

        os.symlink('C++/pbs.py', 'src/pbs.py')

    elif LooseVersion(PBS_VERSION) >= LooseVersion('2.4'):
        TORQUE_VERSION='TORQUE_2'
        SOURCE_FILE='src/C/pbs_wrap.c'
        PBS_PYTHON_INCLUDE_DIR = 'src/C'
        # Older pbs-config yielded some link line info instead of just the libraries
        PBS_LIBS = 'torque'

        os.symlink('C/pbs.py', 'src/pbs.py')

    else:
        print "Version: %s is not supported" %(PBS_VERSION)
        sys.exit(1)

    INCLUDE_DIR = '/usr/include/torque'

    setup (
        name = 'pbs_python',
        version = VERSION,
        description = 'openpbs/torque python interface',
        license = 'LGPLV3',
        author = 'Bas van der Vlies',
        author_email = 'bas.vandervlies@surfsara.nl',
        url = 'http://oss.trac.surfsara.nl/pbs_python',


        extra_path = 'pbs',
            package_dir = { '' : SOURCE_DIR },
            py_modules = [ 'pbs',  'PBSQuery' ],

        ext_modules = [
            Extension( '_pbs', [SOURCE_FILE],
                define_macros =  [ (TORQUE_VERSION, None) ],
                include_dirs = [ INCLUDE_DIR, PBS_PYTHON_INCLUDE_DIR ],
                library_dirs = [ PBS_LIB_DIR ],
                libraries = [ PBS_LIBS ],
                )
        ]
    )
