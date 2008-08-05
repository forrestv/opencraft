def health_bar(length, fraction, view): pass


def progress_bar(a, view):
    s = view.sprites['ProgressEmpty'].copy()
    s.blit(view.sprites['ProgressFull'],(0,0), (0,0,s.get_width()*a,s.get_height()))
    return s
