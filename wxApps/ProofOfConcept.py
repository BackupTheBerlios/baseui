# The next 2 lines enable python to find all modules above!
import sys
sys.path.append("..")

import BuildHelpers


print 'BaseUI is at Revision:', BuildHelpers.get_revision('..')
raw_input('give <RETURN> to exit...')
