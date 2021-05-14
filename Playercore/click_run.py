import subprocess
import sys,os
ret = subprocess.call(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),"click_run.bat")+ ' "'+os.path.join(os.path.abspath('.'),sys.argv[1])+'"',shell=True)

