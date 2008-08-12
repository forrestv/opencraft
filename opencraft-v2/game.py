#!/usr/bin/python

use_psyco = False
psyco_log = False

profile = False

import psyco
import cProfile

def main():
    if use_psyco:
        psyco.full()
    if psyco_log:
        psyco.log()
        
    global src
    import src
    
    if profile:
        cProfile.run("src.main()", "stats")
    else:
        src.main()
        
if __name__ == "__main__":
    main()
