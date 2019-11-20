import os
import glob
import subprocess
import re

# for top, dirs, nondirs in os.walk("./"):
#     print top, dirs, nondirs
#
# for f in os.listdir("./"):
#     if os.path.isfile(f) and not f.startswith("."):
#         print f

# files = glob.glob('.\\test\\x*')
# files = files.sort(key=lambda x: int(x[2:]))
# print files
# print os.path.exists('test1*')
files = glob.glob('t*')
s = 'aaa'
# print 'asdfg'[len(s):]
li = set()
li.add(1)
print li
print 'ADDSdsdf'.lower()

mat = re.match(r'(REP) {4}(RUNNING) {4}(.+) {4}', 'REP    RUNNING    R_ZG_ZD1    12')
if mat:
    print mat.group(1)
    print mat.group(3).endswith(('1','2','3','4','5'))
    print mat.groups()


