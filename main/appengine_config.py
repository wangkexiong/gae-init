# coding: utf-8

import os
import sys

from path_util import sys_path_insert


# https://github.com/jschneier/django-storages/issues/281
import tempfile
import tempfile2
tempfile.SpooledTemporaryFile = tempfile2.SpooledTemporaryFile

if os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine'):
  sys_path_insert('lib.zip')
else:
  # For pycharm debugging purpose:
  from distutils.sysconfig import get_python_lib

  site_dir = get_python_lib()
  use_site_dir = True

  # Workaround for flask working after 0.11.x
  #     Fix for msvcrt import error (issue #526) (#527)
  if os.name == 'nt':
    os.name = None
    sys.platform = ''

  for p in os.listdir('lib'):
    if p.endswith('.pyc'):
      continue

    if not os.path.exists(site_dir + os.sep + p):
      use_site_dir = False
      break

  if use_site_dir:
    sys.path.insert(0, site_dir)
  else:
    from google.appengine.tools.devappserver2.python.runtime import stubs
    import re

    re_ = stubs.FakeFile._skip_files.pattern.replace('|^lib/.*', '')
    re_ = re.compile(re_)
    stubs.FakeFile._skip_files = re_
    sys_path_insert('lib')

# Personal additional libraries
sys_path_insert('libx')


def webapp_add_wsgi_middleware(app):
  from google.appengine.ext.appstats import recording
  app = recording.appstats_wsgi_middleware(app)
  return app
