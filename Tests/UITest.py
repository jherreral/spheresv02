import ui

# Crear screen para los objetos UI
ui.pygame.init()
ui.pygame.event.set_blocked([ui.pygame.MOUSEMOTION, ui.pygame.ACTIVEEVENT])
size = 800, 600
screen = ui.pygame.display.set_mode(size)
ui.Button._screen = screen

