#!/usr/bin/python

def main():
    use_psyco = False
    log = False
    profile = False
    
    if use_psyco:
        import psyco
        psyco.full()
        if log:
            psyco.log()
    global src
    import src.main
    
    if profile:
        import cProfile
        cProfile.run("src.main.main()","stats")
    else:
        src.main.main()
        
if __name__ == "__main__":
    main()
