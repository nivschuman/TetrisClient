from Game import Game
from Server import Server


try:
    game = Game()
    game.main_menu()
except ConnectionRefusedError:
    print("Cannot play because server is offline niv")
