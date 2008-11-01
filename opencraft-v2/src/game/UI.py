class UI(object):
    def update(self, gamestate):
        self
    def draw(self, surface, gamestate):
        self.camera.draw(surface)
        if self.selection:
            pygame.draw.rect(view.screen, (16,252,24), self.selection, 1)
        #surface.blit(read.
    def get_orders(self):
        return []
        
