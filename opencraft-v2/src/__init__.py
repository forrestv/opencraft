import os
import pygame
import read, ui
import ui.GlxMenu
import ui.Video
import music

def display_image(image):
    ui.display.blit(image, ui.get_center_coords(image.get_size(), ui.display.get_size()))
    pygame.display.update()

def play_introduction():
    music.fadeout()
    ui.Video.Video("smk\\blizzard.smk")
    ui.Video.Video("smk\\starxintr.smk")
    music.start("music\\title.wav")

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    pygame.display.init()
    pygame.mixer.init(44100)
    #pygame.mouse.set_visible(False)
    pygame.display.set_caption("Opencraft")
    pygame.display.set_icon(read.read_exe_icon("files\\starcraft.exe"))
    image = read.read_pcx("glue\\title\\title.pcx")
    music.start("music\\title.wav")
    ui.init()
    display_image(image)
    
    import Config
    
    if not Config.config.introduction_played:
        play_introduction()
        Config.config.introduction_played = True
    
    def campaign_editor(): print "campaign editor"
    def credits(): print "credits"
    
    
    ui.GlxMenu.GlxMenu("rez\\glumain.bin", "glue\\palmm\\backgnd.pcx", {
        3: lambda: ui.GlxMenu.GlxMenu("rez\\gluexpcmpgn.bin", "glue\\palcs\\backgnd.pcx", {
            5: lambda: 0, # save
            6: lambda: 0, # protoss
            7: lambda: 0, # terran
            8: lambda: 0, # zerg
            10: lambda: ui.GlxMenu.GlxMenu("rez\\glucreat.bin", "glue\\palcs\\backgnd.pcx", {
                12: lambda: credits(),
            }).execute(),
        }).execute(),
        4: lambda: ui.GlxMenu.GlxMenu("rez\\gluconn.bin", "glue\\palnl\\backgnd.pcx", {
            321312: "a",
        }).execute(),
        5: campaign_editor,
        8: play_introduction,
        9: lambda: ui.GlxMenu.GlxMenu("rez\\credits.bin", "glue\\palmm\\backgnd.pcx", {}).execute(),
    }).execute()
