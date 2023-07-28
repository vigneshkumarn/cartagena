import random

class Player:
    def __init__(self, name, strategy):
        self.hand = []
        self.positions = [0] * 3
        self.name = name
        self.strategy = strategy

class Strategy:
    def __init__(self, bw, pw, cw, penality):
        self.bw = bw 
        self.pw = pw 
        self.cw = cw
        self.penality = penality

class Cartagena:
    def __init__(self, num_players, player_1, player_2):
        self.num_players = num_players
        self.symbols = ['A', 'B', 'C', 'D', 'E', 'F']
        self.cards = ['A', 'B', 'C', 'D', 'E', 'F'] * 17
        template = ['B', 'D', 'A', 'F', 'C', 'E', 'B', 'F', 'A', 'C', 'E', 'D']
        self.board = ['Jail'] + template + ['Boat']
        self.player_1 = player_1
        self.player_2 = player_2

    def initialize_game(self):
        random.shuffle(self.cards)
        self.player_1.hand = self.cards[:6]
        self.player_2.hand = self.cards[6:12]
        self.cards = self.cards[12:]

    def find_possible_spot(self, current_position, computer_positions, human_positions):
        for backward_position in range(current_position - 1, 0, -1):
            occupied_pirates = computer_positions.count(backward_position) + human_positions.count(backward_position)
            if occupied_pirates in [1,2]:
                return backward_position, occupied_pirates
        return None, None
            
    def find_next_spot(self, player, computer_positions, human_positions, card, pirate_index):
        if player == 'Computer':
            current_position = computer_positions[pirate_index]
        else:
            current_position = human_positions[pirate_index]
        for position in range(current_position+1, len(self.board)):
            #ensure spot is available
            if (self.board[position] == 'Boat') or (self.board[position] == card and (computer_positions + human_positions).count(position) < 3):
                return position

    def move_computer(self, max_player, min_player):
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        depth = 3
        strategy = max_player.strategy
        #eval, best_move = self.minimax(self.computer_hand, self.human_hand, self.computer_positions, self.human_positions, True, alpha, beta, depth)
        eval, best_move = self.minimax(max_player.hand, min_player.hand, max_player.positions, min_player.positions, True, alpha, beta, depth, strategy)
        if best_move is not None:
            # print(best_move)
            if best_move['card_index'] != -1:
                card_index = best_move['card_index']
                #self.computer_hand.pop(card_index)
                max_player.hand.pop(card_index)
            else:
                occupied_pirates = best_move['occupied_pirates']
                if occupied_pirates == 1:
                    new_card = self.cards.pop()
                    max_player.hand.append(new_card)
                elif occupied_pirates == 2:
                    new_card_1 = self.cards.pop()
                    new_card_2 = self.cards.pop()
                    #self.computer_hand.append(new_card_1)
                    #self.computer_hand.append(new_card_2)
                    max_player.hand.append(new_card_1)
                    max_player.hand.append(new_card_2)
            pirate_index = best_move['pirate_index']
            #self.computer_positions[pirate_index] = best_move['next_position']
            max_player.positions[pirate_index] = best_move['next_position']

    def move_computer_1(self):
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        depth = 3
        strategy = self.player_2.strategy
        # eval, best_move = self.minimax(self.human_hand, self.computer_hand, self.human_positions, self.computer_positions, True, alpha, beta, depth)
        eval, best_move = self.minimax(self.player_2.hand, self.player_1.hand, self.player_2.positions, self.player_1.positions, True, alpha, beta, depth, strategy)
        if best_move is not None:
            # print(best_move)
            if best_move['card_index'] != -1:
                card_index = best_move['card_index']
                #self.human_hand.pop(card_index)
                self.player_2.hand.pop(card_index)
            else:
                occupied_pirates = best_move['occupied_pirates']
                if occupied_pirates == 1:
                    new_card = self.cards.pop()
                    #self.human_hand.append(new_card)
                    self.player_2.hand.append(new_card)
                elif occupied_pirates == 2:
                    new_card_1 = self.cards.pop()
                    new_card_2 = self.cards.pop()
                    # self.human_hand.append(new_card_1)
                    # self.human_hand.append(new_card_2)
                    self.player_2.hand.append(new_card_1)
                    self.player_2.hand.append(new_card_2)
            pirate_index = best_move['pirate_index']
            # self.human_positions[pirate_index] = best_move['next_position']
            self.player_2.positions[pirate_index] = best_move['next_position']

    def move_human(self):
        # add checks to see if the player is not already on boat and card index and card is present
        card_index = int(input("Enter the index of the card you want to play (or -1 to move backwards): "))
        pirate_index = int(input("Enter the index of the pirate you want to move: "))
        # if self.human_positions[pirate_index] == len(self.board)-1:
        #     print('The player is already on the boat cant move him')
        #     return
        if card_index not in range(-1, len(self.player_2.hand)):
            print('Invalid card index')
            return

        if card_index == -1:
            # Move backwards and collect a card
            current_position = self.player_2.positions[pirate_index]
            backward_position, occupied_pirates = self.find_possible_spot(current_position, self.player_1.positions, self.player_2.positions)
            if occupied_pirates == 1:
                new_card = self.cards.pop()
                self.player_2.hand.append(new_card)
                self.player_2.positions[pirate_index] = backward_position
                moved_back = True
            elif occupied_pirates == 2:
                new_card_1 = self.cards.pop()
                new_card_2 = self.cards.pop()
                self.player_2.hand.append(new_card_1)
                self.player_2.hand.append(new_card_2)
                self.player_2.positions[pirate_index] = backward_position
            else:
                print('No suitable spot to move back')

        else:
            # Play a card and move forward
            card = self.player_2.hand[card_index]
            next_position = self.find_next_spot('Human', self.player_1.positions, self.player_2.positions, card, pirate_index)
            self.player_2.positions[pirate_index] = next_position
            self.player_2.hand.pop(card_index)
            # can show sucess msg and board
     
    def minimax(self, computer_hand, human_hand, computer_positions, human_positions, is_maximizing_player, alpha, beta, depth, strategy):
        if depth == 0 or self.check_win(computer_positions) or self.check_win(human_positions):
            return self.evaluate_position(computer_hand, human_hand, computer_positions, human_positions, strategy), None

        if is_maximizing_player:
            max_eval = float('-inf')
            best_move = None

            # forward movement
            for card_index, card in enumerate(computer_hand):
                for pirate_index in range(len(computer_positions)):
                    if computer_positions[pirate_index] < len(self.board) - 1: # to check if pirate is not already on boat
                        next_position = self.find_next_spot('Computer', computer_positions, human_positions, card, pirate_index)
                        #print(f"pitate_index: {pirate_index}, card: {card}, next_position: {next_position}")
                        if next_position < len(self.board):
                            new_computer_positions = computer_positions[:]
                            new_computer_positions[pirate_index] = next_position
                            eval, _ = self.minimax(computer_hand[:card_index] + computer_hand[card_index + 1:], human_hand, new_computer_positions, human_positions, False, alpha, beta, depth - 1, strategy)
                            if eval >= max_eval:
                                max_eval = eval
                                best_move = {'card_index': card_index, 'pirate_index': pirate_index, 'next_position': next_position, 'depth': depth} #no need to return best move
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
                        
            # Backward movement
            for pirate_index in range(len(computer_positions)):
                current_position = computer_positions[pirate_index]
                # if current_position == len(self.board) - 1:
                #     continue
                backward_position, occupied_pirates = self.find_possible_spot(current_position, computer_positions, human_positions)

                if occupied_pirates == 1:
                    new_card = self.cards.pop()
                    computer_hand.append(new_card)
                    computer_positions[pirate_index] = backward_position
                    eval, _ = self.minimax(computer_hand, human_hand, computer_positions, human_positions, False, alpha, beta, depth - 1, strategy)
                    self.cards.append(new_card) # add back the card
                    computer_hand.pop()
                    computer_positions[pirate_index] = current_position
                    if eval >= max_eval:
                        max_eval = eval
                        best_move = {'card_index': -1, 'pirate_index': pirate_index, 'next_position': backward_position, 
                                     'occupied_pirates': occupied_pirates}

                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break

                elif occupied_pirates == 2:
                    new_card_1 = self.cards.pop()
                    new_card_2 = self.cards.pop()
                    computer_hand.append(new_card_1)
                    computer_hand.append(new_card_2)
                    computer_positions[pirate_index] = backward_position
                    eval, _ = self.minimax(computer_hand, human_hand, computer_positions, human_positions, False, alpha, beta, depth - 1, strategy)
                    self.cards.append(new_card_2) 
                    self.cards.append(new_card_1)
                    computer_hand.pop() 
                    computer_hand.pop() 
                    computer_positions[pirate_index] = current_position
                    if eval > max_eval:
                        max_eval = eval
                        best_move = {'card_index': -1, 'pirate_index': pirate_index, 'next_position': backward_position, 
                                     'occupied_pirates': occupied_pirates, 'depth': depth}

                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            #print(f"Depth: {depth}, max_eval: {max_eval}, best_move: {best_move}")
            return max_eval, best_move

        else: #min turn
            min_eval = float('inf')
            best_move = None

            # forward movement
            for card_index, card in enumerate(human_hand):
                for pirate_index in range(len(human_positions)):
                    if human_positions[pirate_index] < len(self.board) - 1: # to check if not on boat
                        next_position = self.find_next_spot('Human', computer_positions, human_positions, card, pirate_index)
                        
                        if next_position < len(self.board):
                            new_human_positions = human_positions[:]
                            new_human_positions[pirate_index] = next_position
                            eval, _ = self.minimax(computer_hand, human_hand[:card_index] + human_hand[card_index + 1:], computer_positions, new_human_positions, True, alpha, beta, depth - 1, strategy)
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break

            # Backward movement
            for pirate_index in range(len(human_positions)):
                current_position = human_positions[pirate_index]
                # if current_position == len(self.board) - 1:
                #     continue
                backward_position, occupied_pirates = self.find_possible_spot(current_position, computer_positions, human_positions)
                if occupied_pirates == 1:
                    new_card = self.cards.pop()
                    human_hand.append(new_card)
                    human_positions[pirate_index] = backward_position
                    eval, _ = self.minimax(computer_hand, human_hand, computer_positions, human_positions, False, alpha, beta, depth - 1, strategy)
                    self.cards.append(new_card) # add back the card
                    human_hand.pop()
                    human_positions[pirate_index] = current_position
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break

                elif occupied_pirates == 2:
                    new_card_1 = self.cards.pop()
                    new_card_2 = self.cards.pop()
                    human_hand.append(new_card_1)
                    human_hand.append(new_card_2)
                    human_positions[pirate_index] = backward_position
                    eval, _ = self.minimax(computer_hand, human_hand, computer_positions, human_positions, False, alpha, beta, depth - 1, strategy)
                    self.cards.append(new_card_1) 
                    self.cards.append(new_card_2)
                    human_hand.pop() 
                    human_hand.pop() 
                    human_positions[pirate_index] = current_position
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break

            return min_eval, best_move
        
    def evaluate_position(self, computer_hand, human_hand, computer_positions, human_positions, strategy):
        boat_weight = strategy.bw  # Weight for reaching the boat
        card_weight = strategy.cw  # Weight for collecting cards
        computer_score = sum(1 for pos in computer_positions if pos == len(self.board) - 1)
        human_score = sum(1 for pos in human_positions if pos == len(self.board) - 1)
        if computer_score == len(computer_positions):
            return float('inf')
        elif human_score == len(human_positions):
            return float('-inf')
        computer_cards = len(computer_hand)
        human_cards = len(human_hand)
        computer_penality = 0
        human_penality = 0
        progress_weight = strategy.pw

        if computer_cards < (6 - computer_score):
            computer_penality = -strategy.penality 
        elif human_cards < (6 - human_score):
            human_penality = -strategy.penality
        # Calculate the weighted scores
        computer_score = computer_score * boat_weight + computer_cards * card_weight + computer_penality + (sum(computer_positions) * progress_weight)
        human_score = human_score * boat_weight + human_cards * card_weight + human_penality + (sum(human_positions) * progress_weight)
        return computer_score - human_score 
            
    def play(self, display = True):
        self.initialize_game()
        if display:
            print('Initial State')
            print('*************')
            self.display_game_state()
            print('\n')
        while True:
            # print("\nComputer's Turn:")
            self.move_computer(self.player_1, self.player_2)
            if display:
                print("\nComputer's Turn:")
                self.display_game_state()

            if self.check_win(self.player_1.positions):
                if display:
                    print("Computer wins!")
                return(0)
                break

            self.move_computer(self.player_2, self.player_1)
            if display:
                print("\nHuman's Turn:")
                self.display_game_state()

            if self.check_win(self.player_2.positions):
                if display:
                    print("Human wins!")
                return(1)
                break

    def check_win(self, positions):
        return all(position == len(self.board) - 1 for position in positions)

    def display_game_state(self):
        print("Board:", self.board)
        print("Computer's Hand:", self.player_1.hand)
        print("Computer's Positions:", self.player_1.positions)
        print("Human's Hand:", self.player_2.hand)
        print("Human's Positions:", self.player_2.positions)

    def human_play(self):
        self.initialize_game()
        print('Initial State')
        print('*************')
        self.display_game_state()
        print('\n')
        while True:
            print("\nComputer's Turn:")
            self.move_computer(self.player_1, self.player_2)
            self.display_game_state()

            if self.check_win(self.player_1.positions):
                print("Computer wins!")
                break

            print("\nHuman's Turn:")
            self.move_human()
            self.display_game_state()

            if self.check_win(self.player_2.positions):
                print("Human wins!")
                break

    def test_method(self, hand):
        hand.pop()


def simulation(times, display_result):
    result = [0] * 2
    st = Strategy(1,0.5,1,5)
    st1 = Strategy(3,0.5,1,2)
    for i in range(times):
        player_1 = Player('p1', st)
        player_2 = Player('p2', st1)
        game = Cartagena(2, player_1, player_2)
        x = game.play(display_result)
        #print("i:", i, "result:", x)
        result[x] += 1 
    
    print("Total Plays:", times)
    print(f"{player_1.name} win percentage: {(result[0]/ times) * 100} %")
    print(f"{player_2.name} win percentage: {(result[1]/times) * 100} %")

# # Create a Cartagena game instance with 2 players
# st = Strategy(1,0.5,1,5)
# player_1 = Player('p1', st)
# player_2 = Player('p2', None)
# game = Cartagena(2, player_1, player_2)
# game.human_play()


simulation(10, False)
