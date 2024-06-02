from random import randint

class LFG:
    def __init__(self, deck, state):
        self.deck = deck
        self.N = 2**24 - 1
        if len(state) == 0:
            self.state = [randint(0, self.N) for _ in range(10)]
        else:
            self.state = state

    def next(self):
        
        x = (self.state[0] + self.state[3] + self.state[9]) % self.N
        state_new = [int(self.state[i]) for i in range(1, 10)]
        self.state = state_new
        self.state.append(x)

        return x 
    
    def first_draw(self, n):
        first_draw = []
        self.x = self.next()
        for _ in range(n):

            first_draw.append(self.deck[self.x % len(self.deck)])
            self.deck.remove(self.deck[self.x % len(self.deck)])

        return first_draw
    
    def second_draw(self, n):
        second_draw = []

        for _ in range(n):

            second_draw.append(self.deck[self.x % len(self.deck)])
            self.deck.remove(self.deck[self.x % len(self.deck)])
                    
        return second_draw
    
    def get_state(self):
        return self.state