import pygame
from .. import read
from .. import cdict
import ui

import font

def blend(amt, less, more):
    if amt < 1./256: return less
    if amt > 255./256: return more
    try:
        l = pygame.surfarray.pixels3d(less).astype('f')
        la = pygame.surfarray.pixels_alpha(less).astype('f')
        m = pygame.surfarray.pixels3d(more).astype('f')
        ma = pygame.surfarray.pixels_alpha(more).astype('f')
        final = pygame.Surface(less.get_size(), pygame.SRCALPHA)
        f = pygame.surfarray.pixels3d(final)
        fa = pygame.surfarray.pixels_alpha(final)
        f[:,:,:] = (l*(1-amt)+m*amt).astype('b')
        fa[:,:] = (la*(1-amt)+ma*amt).astype('b')
        return final
    except:
        if amt < 1./2: return less
        return more
        
class GlxMenu(ui.UI):
    def __init__(self, file, bg, actions):
        ui.UI.__init__(self)
        self.node = read.read_bin(file)
        self.bg = bg
        self.actions = actions
        self.mousemotion(pygame.mouse.get_pos(), None, None)
        palette = "glue\\palmm\\tfont.pcx"
        self.icache = cdict.cdict(lambda x: read.read_pcx(x))
        self.vcache = cdict.cdict(lambda x: read.read_smk(x))
        self.tcache = cdict.cdict(lambda x: font.render(x[0], palette, x[1]))
        for n in self.node.children:
            n.activeblend = 0
        self.add_call(self.work, 1./11)
    
    def work(self):
                print "WORK"
                i = self.icache[self.bg]
                self.display.blit(i, (0, 0))
                for n in self.node.children:
                    self.draw_node(n)
                self.update()
    
    def draw_node(self, n):
        n.activeblend = (n.active+n.activeblend)/2.
        if not n.visible: return
        for m in n.children:
            v = self.vcache[m.text]
            if not m.play_on_hover or n.active:
                self.display.blit(v.video, (n.x+m.x, n.y+m.y))
            v.next()
        if n.type == 5:
            i = self.icache[n.text]
            #if n.hide_color_0_edges:
            i.set_colorkey(0)
            self.display.blit(i, (n.x, n.y))
        elif n.type == 14 or n.type == 11 or n.type == 10 or n.type == 9:
            if n.type == 11:
                t = "Version 1.15.2"
                align = "right"
            else:
                t = str(n.text)
                align = "left"
            if n.has_hotkey:
                t = t[1:]
            i = self.tcache["10" if n.smallest_font else "16x", t]
            if n.responds_mouse:
                t = "\x04"+t.replace("\x01","")
                on = self.tcache["10" if n.smallest_font else "16x", t]
                i = blend(n.activeblend, i, on)
            if align == "right":
                new = pygame.Surface((n.width-2, n.height),pygame.SRCALPHA)
                new.blit(i, (new.get_width()-i.get_width(),0))
                i = new
            self.display.blit(i, (n.x+n.textx, n.y+n.texty))
        else:
            pygame.draw.rect(self.display, (255,0,0), (n.x,n.y,n.width,n.height),  1)
            #n.text = str(n.type)
            #n.type = 14
    def pressed(self, node):
        if node.cancel:
            self.run = False
            return
        if node.index in self.actions:
            self.pause = True
            self.actions[node.index]()
            self.pause = False
        else:
            print "Action not defined for button", node.index
    
    def mousebuttondown(self, pos, button):
        for n in self.node.children:
            if n.responds_mouse:
                if pygame.rect.Rect(n.x+n.mousex1,n.y+n.mousey1,n.mousex2-n.mousex1,n.mousey2-n.mousey1).collidepoint(pos):
                    self.pressed(n)
                    break
    def mousemotion(self, pos, rel, buttons):
        if not pygame.mouse.get_focused():
            for n in self.node.children:
                n.active = False
        else:
            for n in self.node.children:
                n.active = pygame.rect.Rect(n.x+n.mousex1,n.y+n.mousey1,n.mousex2-n.mousex1,n.mousey2-n.mousey1).collidepoint(pos)
    def activeevent(self, state, gain):
        self.mousemotion(pygame.mouse.get_pos(), None, None)
