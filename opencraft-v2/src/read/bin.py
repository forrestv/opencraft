import struct

class Node:
    def __init__(self, file, offset=0, level=0):
        if isinstance(file, str):
            file = open(f)
        file.seek(offset)
        
        if level == 2:
            st = "<15H"
            s = "0, 1, smk?, play_on_hover, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31"
        else:
            st = "<12HI2Hh26H"
            s = "0, disabled, 2, visible, responds_mouse, 5, cancel, no_over_sound, 8, has_hotkey, smallest_font, larger_font, 12, hide_color_0_edges, largest_font, 15, smaller font, 17, translucency_effect, default, bring_to_front, center, right, center, smk_on_top?, brighten_on_mouseover?, 26, 27, 28, 29, no_click_sound, 31"
            
        d = file.read(struct.calcsize(st))
        d = struct.unpack(st, d)
        if level == 2:
            NextOffset, Unknown2, Flags, Unknown4, Unknown5, TextOffset, Unknown7, Unknown8, Unknown9, X, Y, Unknown12, Unknown13, Unknown14, Unknown15 = d
            X1 = X
            Y1 = Y
            X2 = None
            Y2 = None
            Width = None
            Height = None
            ChildOffset = 0
            Type = None
            UnknownIndex = None
            TextX1 = None
            TextY1 = None
            DialogWidth_MouseX1 = None
            DialogWidth_MouseY1 = None
            MouseX2 = None
            MouseY2 = None
        else:
            NextOffset, Unknown2, X1, Y1, X2, Y2, Width, Height, Unknown9, Unknown10, \
                TextOffset, Unknown12, Flags, Unknown15, Unknown16, UnknownIndex, Type, Unknown19, Unknown20, Unknown21, \
                Unknown22, Unknown23, Unknown24, Unknown25, Unknown26, Unknown27, DialogWidth_MouseX1, DialogWidth_MouseY1, MouseX2, MouseY2, \
                Unknown32, Unknown33, ChildOffset, Unknown35, TextX1, TextY1, TextX2, TextY2, Unknown40, Unknown41, \
                Unknown42, Unknown43 = d
        for k,v in locals().items():
            if k in ("Flags","Height","Width","Type","file","st","d","UnknownIndex","X1","X2","Y1","Y2","level","offset","self","NextOffset","TextOffset","X","Y","ChildOffset","s"): continue
            setattr(self, "bad_"+k,v)
        self.x = X1
        self.y = Y1
        self.x1 = X2
        self.y1 = Y2
        self.width = Width
        self.height = Height
        self.type = Type
        self.index = UnknownIndex
        self.textx = TextX1
        self.texty = TextY1
        self.mousex1 = DialogWidth_MouseX1
        self.mousey1 = DialogWidth_MouseX1
        self.mousex2 = MouseX2
        self.mousey2 = MouseY2
        
        s = s.split(", ")
        self.bad = []
        for i in range(32):
            c = bool(Flags & (2**i))
            try:
                int(s[i])
            except ValueError:
                pass
            else:
                if c:
                    self.bad.append((i))
                continue
            setattr(self, s[i], c)
            
        if TextOffset:
            file.seek(TextOffset)
            s = ""
            while True:
                c = file.read(1)
                if c == "\0" or c == "": break
                s = s+c
            self.text = s
        else:
            self.text = None
            
        if level == 0:
            assert NextOffset == 0
        else:
            self.NextOffset = NextOffset
            
        self.children = []
        if ChildOffset:
            self.children.append(Node(file, ChildOffset, level+1))
            while self.children[-1].NextOffset:
                self.children.append(Node(file, self.children[-1].NextOffset, level+1))
            for c in self.children:
                del c.NextOffset
                
# Testing code

def bin(n):
    t = {
        '0': '000',
        '1': '001',
        '2': '010',
        '3': '011',
        '4': '100',
        '5': '101',
        '6': '110',
        '7': '111',
    }
    n = oct(n)
    r = ''
    for i in n:
        r = r + t[i]
    return str(int(r))
    
def print_tree(t, indent=0):
    print '    '*indent+repr(t.text)
    for k in sorted(dir(t)):
        if k[0] == '_' or k == 'children' or k =='text': continue
        v = getattr(t,k)
        if v:
            print '    '*(indent+2), k, v
    for i in t.children:
        print_tree(i, indent + 1)
        
if __name__ == "__main__":
    import sys
    f = sys.argv[1]
    t = Node(f)
    print_tree(t)
    sys.exit()
    import pygame
    import random
    d = pygame.display.set_mode((t.width,t.height))
    for n in t.children:
        pygame.draw.rect(d, [random.random()*255 for i in range(3)], (n.x,n.y,n.width,n.height))
        for j in n.children:
            pygame.draw.rect(d, [random.random()*255 for i in range(3)], (n.x+j.x,n.y+j.y,10,10))
            
    while True: pygame.display.update()
    
