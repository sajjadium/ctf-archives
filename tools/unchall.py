#!/usr/bin/env python3

import os
import sys
import tempfile

archive_filename = sys.argv[1]
dst_dir = archive_filename.split('.')[0]
os.system('mkdir "%s"' % dst_dir)

with tempfile.TemporaryDirectory() as tmp_path:
  if archive_filename.endswith('.zip'):
    os.system('unzip -d %s "%s"' % (tmp_path, archive_filename))

  final_path = tmp_path
  while True:
    children = os.listdir(final_path)
    if len(children) == 0 or len(children) > 1:
      break

    child_path = os.path.join(final_path, children[0])

    if not os.path.isdir(child_path):
      break

    final_path = child_path

  os.system('mv %s/* %s' % (final_path, dst_dir))

