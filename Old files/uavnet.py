#!/usr/bin/env python
import os
import subprocess

from subprocess import call

command = 'python adhocUAV.py'
password = 'Oneiros89!'

# #subprocess.Popen(command , shell=True,stdout=subprocess.PIPE)
# os.system(command)
# os.system('pingall')

# call(["wireshark"])
# call(["ryu-manager", "--observe-links", "simple_switch_stp.py"])
# call(["python", "adhocUAV.py"])

subprocess.call(['gnome-terminal', '-x', 'wireshark'])
subprocess.call(['gnome-terminal', '-x', 'ryu-manager --observe-links simple_switch_stp.py'])
