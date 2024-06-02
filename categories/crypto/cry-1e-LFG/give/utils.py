from LFG import LFG
import os

def gen_draw(deck, first_state):
    generator = LFG(deck, first_state)
    first_draw = generator.first_draw(5)
    second_draw = generator.second_draw(5)
    state = generator.get_state()

    return first_draw, second_draw, state


def decomp(drawFinal):
    value = []
    color = []

    for carte in drawFinal:
        value.append(carte.split("-")[0])
        color.append(carte.split("-")[1])

    for e,i in zip(value, range(0,5)):

        try:
            value[i] = int(e)

        except:
            if e == "J":
                value[i] = 11
            elif e == "Q":
                value[i] = 12
            elif e == "K":
                value[i] = 13
            elif e == "A":
                value[i] = 14
            else:
                continue
    return value,color

#---------------------------PARE-----------------------

def Pare(drawFinal):
        value,color = decomp(drawFinal)
        valueDistinctes = set(value)
        compte = []

        for i in valueDistinctes:
            compte.append(value.count(i))

        compte.sort()

        if len(valueDistinctes) == 4 and compte == [1,1,1,2]:
            return True
        
        else:
            return False

#---------------------------DOUBLE PARE-----------------------

def DoublePare(drawFinal):
        value,color = decomp(drawFinal)
        valueDistinctes = set(value)
        compte = []

        for i in valueDistinctes:
            compte.append(value.count(i))

        compte.sort()

        if len(valueDistinctes) ==3 and compte == [1,2,2]:
            return True
        
        else:
            return False

#---------------------------BRELAN-----------------------

def brelan(drawFinal):
        value,color = decomp(drawFinal)
        valueDistinctes = set(value)
        compte = []

        for i in valueDistinctes:
            compte.append(value.count(i))
        
        compte.sort()
        
        if len(valueDistinctes) == 3 and compte == [1,1,3]:
            return True
        
        else:
            return False

#---------------------------CARRE-----------------------

def carre(drawFinal):
        value,color = decomp(drawFinal)
        valueDistinctes = set(value)
        compte = []

        for i in valueDistinctes:
            compte.append(value.count(i))
        
        compte.sort()
        
        if len(valueDistinctes) == 2 and compte == [1,4]:
            return True
        
        else:
            return False

#---------------------------Straight-----------------------

def Straight(drawFinal):
    value,color = decomp(drawFinal)
    value.sort()
    int_value = []

    for i in value:
        int_value.append(int(i))

    if int_value[0] + 4 == int_value[1] + 3 == int_value[2] + 2 == int_value[3] + 1 == int_value[4]:
        return True
    else: 
        return False

#---------------------------FLUSH-----------------------

def flush(drawFinal):
    value,color = decomp(drawFinal)
    color.sort()
    n = 5
    prev = -10
    count = 0
    flag = 0

    for item in color:
        if item == prev:
            count = count+1
        else:
            count = 1
        prev = item

        if count == n:
            flag = 10
            return True
    
    if flag == 0:
        return False

#---------------------------FULL-----------------------

def full(drawFinal):
        value,color = decomp(drawFinal)
        valueDistinctes = set(value)
        compte = []
        for i in valueDistinctes:
            compte.append(value.count(i))
        compte.sort()
        if len(valueDistinctes) == 2 and compte == [2,3]:
            return True
        else:
            return False

#---------------------------Straight FLUSH-----------------------

def Flush(drawFinal):

    if Straight(drawFinal) == True and flush(drawFinal) == True:
        return True

    else:
        return False

#---------------------------Straight FLUSH ROYAL-----------------------

def FlushRoyal(drawFinal):
    value,color = decomp(drawFinal)
    value.sort()

    if value == [10,11,12,13,14] and flush(drawFinal) == True:
        return True

    else:
        return False

#---------------------------CHECK combinations-----------------------

def combinations(drawFinal,mise):

    if FlushRoyal(drawFinal) == True:
        gain = mise * 250
        result = "You have a royal flush, you win {} euros".format(gain)  
        return gain,result

    elif Flush(drawFinal) == True:
        gain = mise * 50
        result = "You have a straight flush, you win {} euros".format(gain)
        return gain,result

    elif carre(drawFinal) == True:
        gain = mise * 25
        result = "You have an edge, you earn {} euros".format(gain)
        return gain,result

    elif full(drawFinal) == True:
        gain = mise * 9
        result = "You have a full, you earn {} euros".format(gain)
        return gain,result

    elif flush(drawFinal) == True:
        gain = mise * 6
        result = "You have a flush, you win: {} euros".format(gain)
        return gain,result

    elif Straight(drawFinal) == True:
        gain = mise * 4
        result = "You have a straight, you win {} euros".format(gain)
        return gain,result
    
    elif brelan(drawFinal) == True:
        gain = mise * 3
        result = "You have a three of a kind have, you win: {} euros".format(gain)
        return gain,result

    elif DoublePare(drawFinal) == True:
        gain = mise * 2
        result = "You have a double pair, you win: {} euros".format(gain)
        return gain,result

    elif Pare(drawFinal) == True:
        gain = mise * 1
        result = "You have a pair, you win: {} euros".format(gain)
        return gain,result
    
    else:
        gain = 0
        result = "Lost"
        return gain, result


def get_flag():
        return os.environ.get('FLAG')

