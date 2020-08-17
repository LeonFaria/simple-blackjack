import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card():
    
    def __init__(self, suit,rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck():
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
                
    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return "The deck has: "+ deck_comp
    
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []  
        self.value = 0 
        self.aces = 0
        
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    
    def __init__(self, total = 500):
        self.total = total
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input("\nPlace your bet : "))
        except ValueError:
            print("\nPlease enter a number!")
        else:
            if chips.bet > chips.total:
                print("\nSorry, you do not have the funds to make this bet. You currently have ",chips.total, " chips")
            else:
                break
                
def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing
    
    while True:
        x = str(input("\nHit or Stand? ")).lower()
        
        if x == "hit":
            hit(deck,hand)
            
        elif x == "stand":
            print("\nPlayer stands. The Dealer will play.")
            playing = False
        
        else:
            print("\nSorry, try again")
            continue
        break
        
def show_some(player,dealer):
    
    print("\nDealer's Hand:")
    print("<card hidden>")
    print("",dealer.cards[1])
    print("\nPlayer's Hand:" , *player.cards, sep="\n")

def show_all(player, dealer):
    
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

def player_busts(player,dealer,chips):
    print("BUST! DEALER WINS!")
    chips.lose_bet()
    print("\nYour winnings: ",chips.total)

def player_wins(player,dealer,chips):
    print("WINNER!")
    chips.win_bet()
    print("\nYour winnings: ",chips.total)

def dealer_busts(player,dealer,chips):
    print("DEALER BUSTS! YOU WIN!")
    chips.win_bet()
    print("\nYour winnings: ",chips.total)
    
def dealer_wins(player,dealer,chips):
    print("DEALER WINS!")
    chips.lose_bet()
    print("\nYour winnings: ",chips.total)
    
def push(player,dealer,chips):
    print("\nDealer and Player tie! It's a push.")
    print("\nYour winnings: ",chips.total)


# The Game

chips = Chips()
bruh = True
while bruh == True:
    
    #####Welcome Message#####
    
    
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\nDealer hits until she reaches 17. Aces count as 1 or 11.')
    
    #####Deck assignment and card dealing#####
    
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    #####Player chip setup#####
    
    print("")
    print("\nYou have {} chips".format(chips.total))
    
    #####Take bet#####
    
    print("\nLets begin.")
    take_bet(chips)
    
    #####Display the hands#####
    
    show_some(player_hand,dealer_hand)
    
    #####Player's Turn#####    

    while playing:
        hit_or_stand(deck,player_hand)
        
        show_some(player_hand,dealer_hand)
        
        
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,chips)
            break

    #####Dealer's Turn#####
            
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
            
        show_all(player_hand,dealer_hand)
        
        #####Outcomes######
        
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,chips)
        
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand,dealer_hand,chips)
            
        elif player_hand.value < dealer_hand.value:
            dealer_wins(player_hand,dealer_hand,chips)
            
        else:
            push(player_hand,dealer_hand,chips)
            
        #####Play again#####
    
    new_game = input("\nWould you like to play again? Enter 'y' or 'n' ")    
    
    if new_game[0] == "y":
        playing = True
        print("\n"*100)
        continue
        
    else:
        print("\nThanks for playing!")
        bruh = False