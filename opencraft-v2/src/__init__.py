import os
import pygame
import read, ui
import music

def display_image(image):
    ui.display.blit(image, ui.get_center_coords(image.get_size(), ui.display.get_size()))
    pygame.display.update()

def play_introduction():
    music.fadeout()
    ui.Video("smk\\blizzard.smk")
    ui.Video("smk\\starxintr.smk")
    music.start("music\\title.wav")

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    pygame.display.init()
    pygame.mixer.init(44100)
    #pygame.mouse.set_visible(False)
    pygame.display.set_caption("Opencraft")
    pygame.display.set_icon(read.read_exe_icon("files\\starcraft.exe"))
    image = read.read_pcx("glue\\title\\title.pcx")
    ui.display = pygame.display.set_mode((640,480))
    music.start("music\\title.wav")
    display_image(image)
    
    import Config
    
    if not Config.config.introduction_played:
        play_introduction()
        Config.config.introduction_played = True
    
    def multiplayer(): print "multiplayer"
    def credits(): print "credits"
    
    
    ui.GlxMenu("rez\\glumain.bin", "glue\\palmm\\backgnd.pcx", {
        3: lambda: ui.GlxMenu("rez\\gluexpcmpgn.bin", "glue\\palcs\\backgnd.pcx", {
            5: lambda: 0, # save
            6: lambda: 0, # protoss
            7: lambda: 0, # terran
            8: lambda: 0, # zerg
            10: lambda: ui.GlxMenu("rez\\glucreat.bin", "glue\\palcs\\backgnd.pcx", {
                12: lambda: credits(),
            }),
        }),
        4: lambda: ui.GlxMenu("rez\\gluconn.bin", "glue\\palnl\\backgnd.pcx", {
            321312: "a",
        }),
        5: lambda: 0, # campaign editor
        8: play_introduction,
        9: lambda: ui.GlxMenu("rez\\credits.bin", "glue\\palmm\\backgnd.pcx", {}),
    }).execute()
