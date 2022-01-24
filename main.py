from Game import Game


try:
    game = Game()
    game.main_menu()
except ConnectionRefusedError:
    print("Cannot play because server is offline")
except KeyboardInterrupt:
    pass
