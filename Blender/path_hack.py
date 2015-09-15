# A quick workaround for path issues
import os
import bge
import site

os.chdir(bge.logic.expandPath('//'))
site.addsitedir(os.getcwd())