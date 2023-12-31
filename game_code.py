import random

class Cartagena:
    def __init__(self, num_players):
        self.num_players = num_players
        self.symbols = ['A', 'B', 'C', 'D', 'E', 'F']
        self.cards = ['A', 'B', 'C', 'D', 'E', 'F'] * 17
        self.board = ['Jail'] + ['A', 'B', 'C', 'D', 'E', 'F'] * 2 + ['Boat']
        self.computer_hand = []
        self.human_hand = []
        self.computer_positions = [0] * 6
        self.human_positions = [0] * 6

    def initialize_game(self):
        random.shuffle(self.cards)
        self.computer_hand = self.cards[:6]
        self.human_hand = self.cards[6:12]
        self.cards = self.cards[12:]

    def move_computer(self):
        max_eval = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        depth = 3
        for card_index, card in enumerate(self.computer_hand):
            for pirate_index in range(len(self.computer_positions)):
                if self.computer_positions[pirate_index] < len(self.board) - 1: # the pirate is not in boat
                    next_position = self.computer_positions[pirate_index] + 1
                    while next_position < len(self.board) and card != self.board[next_position]:
                        next_position += 1
                    
                    if next_position < len(self.board):
                        new_computer_positions = self.computer_positions[:]
                        new_computer_positions[pirate_index] = next_position
                        moved_card = self.computer_hand.pop(card_index) 
                        eval, _ = self.minimax(self.computer_hand[:card_index] + self.computer_hand[card_index + 1:], self.human_hand, new_computer_positions, self.human_positions, False, alpha, beta, depth - 1)
                        self.computer_hand.insert(card_index, moved_card)
                        if eval > max_eval:
                            max_eval = eval
                            best_move = {'card_index': card_index, 'pirate_index': pirate_index, 'next_position': next_position}

                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break

        if best_move is not None:
            card_index = best_move['card_index']
            pirate_index = best_move['pirate_index']
            self.computer_positions[pirate_index] = best_move['next_position']
            self.computer_hand.pop(card_index)

    def move_human(self):
        # add checks to see if the player is not already on boat and card index and card is present
        card_index = int(input("Enter the index of the card you want to play (or -1 to move backwards): "))
        pirate_index = int(input("Enter the index of the pirate you want to move: "))

        if card_index == -1:
            moved_back = False
            # Move backwards and collect a card
            current_position = self.human_positions[pirate_index]
            for position in range(current_position - 1, 1, -1):
                occupied_pirates = self.computer_positions.count(position) + self.human_positions.count(position)
                if occupied_pirates in [1, 2]:
                    if occupied_pirates == 1:
                        new_card = self.cards.pop()
                        self.human_hand.append(new_card)
                        self.human_positions[pirate_index] = position
                    else:
                        new_card_1 = self.cards.pop()
                        new_card_2 = self.cards.pop()
                        self.human_hand.append(new_card_1)
                        self.human_hand.append(new_card_2)
                        self.human_positions[pirate_index] = position
                    break
            if moved_back == False:
                print('No suitable spot to move back')

        else:
            # Play a card and move forward
            card = self.human_hand[card_index]
            success = self.move_pirate(card, 'Human', pirate_index)

            if success:
                self.human_hand.pop(card_index)
                # can show sucess msg and board
     
    def minimax(self, computer_hand, human_hand, computer_positions, human_positions, is_maximizing_player, alpha, beta, depth):
        if depth == 0:
            return self.evaluate_position(computer_positions, human_positions), None

        if is_maximizing_player:
            max_eval = float('-inf')
            best_move = None

            # forward movement
            for card_index, card in enumerate(computer_hand):
                for pirate_index in range(len(computer_positions)):
                    if computer_positions[pirate_index] < len(self.board) - 1:
                        next_position = computer_positions[pirate_index] + 1
                        while next_position < len(self.board) and card != self.board[next_position]:
                            next_position += 1
                        
                        if next_position < len(self.board):
                            new_computer_positions = computer_positions[:]
                            new_computer_positions[pirate_index] = next_position
                            moved_card = computer_hand.pop(card_index)  # Temporarily remove the card from the hand
                            eval, _ = self.minimax(computer_hand[:card_index] + computer_hand[card_index + 1:], human_hand, new_computer_positions, human_positions, False, alpha, beta, depth - 1)
                            computer_hand.insert(card_index, moved_card)
                            if eval > max_eval:
                                max_eval = eval
                                best_move = {'card_index': card_index, 'pirate_index': pirate_index, 'next_position': next_position} #no need to return best move

                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
                        
            # Backward movement
            for pirate_index in range(len(computer_positions)):
                current_position = computer_positions[pirate_index]
                for position in range(current_position - 1, 1, -1):
                    occupied_pirates = computer_positions.count(position) + human_positions.count(position)
                    if occupied_pirates in [1, 2]:
                        if occupied_pirates == 1:
                            new_card = self.cards.pop()
                            computer_hand.append(new_card)
                            computer_positions[pirate_index] = position
                            eval, _ = self.minimax(computer_hand, human_hand, computer_positions, human_positions, False, alpha, beta, depth - 1)
                            self.cards.append(new_card) # add back the card
                            computer_hand.pop()
                            computer_positions[pirate_index] = current_position
                            if eval > max_eval:
                                max_eval = eval
                                best_move = {'card_index': -1, 'pirate_index': pirate_index, 'next_position': position, 'card': card}

                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
                        else:
                            new_card_1 = self.cards.pop()
                            new_card_2 = self.cards.pop()
                            computer_hand.append(new_card_1)
                            computer_hand.append(new_card_2)
                            computer_positions[pirate_index] = position
                            eval, _ = self.minimax(computer_hand, human_hand, computer_positions, human_positions, False, alpha, beta, depth - 1)
                            self.cards.append(new_card_1) 
                            self.cards.append(new_card_2)
                            computer_hand.pop() 
                            computer_hand.pop() 
                            computer_positions[pirate_index] = current_position
                            if eval > max_eval:
                                max_eval = eval
                                best_move = {'card_index': -1, 'pirate_index': pirate_index, 'next_position': position, 'card': card}

                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
                        break

            return max_eval, best_move

        else: #min turn
            min_eval = float('inf')
            best_move = None

            # forward movement
            for card_index, card in enumerate(human_hand):
                for pirate_index in range(len(human_positions)):
                    if human_positions[pirate_index] < len(self.board) - 1:
                        next_position = human_positions[pirate_index] + 1
                        while next_position < len(self.board) and card != self.board[next_position]:
                            next_position += 1
                        
                        if next_position < len(self.board):
                            new_human_positions = human_positions[:]
                            new_human_positions[pirate_index] = next_position
                            moved_card = human_hand.pop(card_index)  # Temporarily remove the card from the hand
                            eval, _ = self.minimax(computer_hand, human_hand[:card_index] + human_hand[card_index + 1:], computer_positions, new_human_positions, True, alpha, beta, depth - 1)
                            human_hand.insert(card_index, moved_card)  # Add the card back to the hand
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break

            #backward movement
            # Backward movement
            for pirate_index in range(len(human_positions)):
                current_position = human_positions[pirate_index]
                for position in range(current_position - 1, 1, -1):
                    occupied_pirates = computer_positions.count(position) + human_positions.count(position)
                    if occupied_pirates in [1, 2]:
                        if occupied_pirates == 1:
                            new_card = self.cards.pop()
                            human_hand.append(new_card)
                            human_positions[pirate_index] = position
                            eval, _ = self.minimax(computer_hand, human_hand, computer_positions, human_positions, False, alpha, beta, depth - 1)
                            self.cards.append(new_card) # add back the card
                            human_hand.pop()
                            human_positions[pirate_index] = current_position
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break
                        else:
                            new_card_1 = self.cards.pop()
                            new_card_2 = self.cards.pop()
                            human_hand.append(new_card_1)
                            human_hand.append(new_card_2)
                            human_positions[pirate_index] = position
                            eval, _ = self.minimax(computer_hand, human_hand, computer_positions, human_positions, False, alpha, beta, depth - 1)
                            self.cards.append(new_card_1) 
                            self.cards.append(new_card_2)
                            human_hand.pop() 
                            human_hand.pop() 
                            human_positions[pirate_index] = current_position
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break
                        break
            return min_eval, best_move

    def evaluate_position(self, computer_positions, human_positions):
        boat_weight = 2  # Weight for reaching the boat
        card_weight = 1  # Weight for collecting cards
        computer_score = sum(1 for pos in computer_positions if pos == len(self.board) - 1)
        human_score = sum(1 for pos in human_positions if pos == len(self.board) - 1)
        computer_cards = len(self.computer_hand)
        human_cards = len(self.human_hand)

        # Special case: One pirate and one card left
        if len(computer_positions) == 1 and computer_cards == 1:
            pirate_index = 0  # Assuming only one pirate for the computer
            current_position = computer_positions[pirate_index]
            card = self.computer_hand[0]

            for position in range(current_position + 1, len(self.board)):
                if self.board[position] == card:
                    break
        else:
            # No matching symbol found after current position, pirate can jump on the boat directly
            computer_score += boat_weight

        # Calculate the weighted scores
        computer_score = computer_score * boat_weight + computer_cards * card_weight
        human_score = human_score * boat_weight + human_cards * card_weight

        return computer_score - human_score
    
    def move_pirate(self, card, player, pirate_index):
        if player == 'Computer':
            positions = self.computer_positions
        else:
            positions = self.human_positions

        current_position = positions[pirate_index]

        for position in range(current_position+1, len(self.board)):
            #ensure spot is available
            if (self.board[position] == 'Boat') or (self.board[position] == card and (self.computer_positions + self.human_positions).count(position) < 3):
                positions[pirate_index] = position
                return True
        
    def play(self):
        self.initialize_game()
        print('Initial State')
        print('*************')
        self.display_game_state()
        print('\n')
        self.move_computer()
        while True:
            print("\nComputer's Turn:")
            self.move_computer()
            self.display_game_state()

            if self.check_win(self.computer_positions):
                print("Computer wins!")
                break

            print("\nHuman's Turn:")
            self.move_human()
            self.display_game_state()

            if self.check_win(self.human_positions):
                print("Human wins!")
                break

    def check_win(self, positions):
        return all(position == len(self.board) - 1 for position in positions)

    def display_game_state(self):
        print("Board:", self.board)
        print("Computer's Hand:", self.computer_hand)
        print("Computer's Positions:", self.computer_positions)
        print("Human's Hand:", self.human_hand)
        print("Human's Positions:", self.human_positions)

# Create a Cartagena game instance with 2 players
game = Cartagena(2)
game.play()