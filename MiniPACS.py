'''
This is the main file that runs the MiniPACS project for the STP Yr2 pratical
computing sessions. If you want to run the whole system then run this file.
'''

import sys
sys.path.append("./modules")
import GUI

if __name__ == "__main__":
    GUI.ShowGui()