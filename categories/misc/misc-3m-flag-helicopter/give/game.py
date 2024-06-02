import sys
import time
import pickle
import collections
import io

class Helicopter:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move_right(self):
        self.x += 1
        self.y += 1

    def show(self):
        print("\r" + " " * self.x + "🚁", flush=True)

class HeroName(pickle.Unpickler): 
     def find_class(self, module, name): 
        if module == 'collections' and '__' not in name:
            return getattr(collections, name)
        raise pickle.UnpicklingError('bad')

def main():
    helicopter = Helicopter()

    while True:
        helicopter.move_right()
        helicopter.show()

        time.sleep(0.1)

        if helicopter.x >= 1000:
            print("\nYou lose!")
            sys.exit()
        if input() == "q":
            player_name = bytes.fromhex(input("Enter name in hex format: "))
            HeroName(io.BytesIO(player_name)).load()


if __name__ == "__main__":
    main()
