from state.state import State

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        
    def update(self, delta_time, actions):
        pass

    def render(self, display):
        display.fill((255,255,255))
        self.game.draw_text(display, "Game States Demo", (0,0,0), 1280/2, 768/2 )