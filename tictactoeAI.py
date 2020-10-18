#when printed, the game board looks like this (instead of the '11', '22', etc. it contains 'X' or 'O' or ' ')
# ---------------
# | 11 | 12 | 13 |
# ---------------
# | 21 | 22 | 23 |
# ---------------
# | 31 | 32 | 33 |
# ---------------
#here 11, 12, 13, 21... are the names of the positions
#variables
#game_dict is a dictionary with the name of the positions as keys and the character on thet position as values
#when a new game starts, the game_dict looks like {'11': " ", '12': " ", '13': " "..., '33': " "}
#valid_positions is a list of all the empty positions (the positions which have the value " " in the game_dict),
#i.e., the positions which are valid for the user and the computer to put their character on

def reset_game(mode):
    #reset the values of positions of the game to " " (if mode != 'pos') or to the name of the position (if mode == 'pos')
    game_dict = {}
    for row in range(1, 4):
        for column in range(1, 4):
            pos = 10 * row + column
            if mode == "pos":
                game_dict[str(pos)] = str(pos)
            else:
                game_dict[str(pos)] = " "
    #return the game postition-value dictionary
    return game_dict

def print_game(game_dict):
    #function specifically made to print the game position-value dictionary in user understandable form
    print()
    print("-------------")
    print("|",game_dict["11"], "|",game_dict["12"], "|",game_dict["13"], "|")
    print("-------------")
    print("|",game_dict["21"], "|",game_dict["22"], "|",game_dict["23"], "|")
    print("-------------")
    print("|",game_dict["31"], "|",game_dict["32"], "|",game_dict["33"], "|")
    print("-------------")
    print()

def take_user_input(question, valid_answers, error):
    #take input from user with custom question, valid answers and error
    while True:
        #ask the question
        response = input(question).strip().upper()
        #check if the answer by user is in valid answers
        if response in valid_answers:
            #if yes, return the user answer
            return response
        else:
            #else print the error string
            print(error)

def think(game_dict, valid_positions, chance, comp_char, user_char, initial, minormax):
    #tictactoe AI using minimax method through recursion
    #minimax algorithm starts here
    scores = []
    for pos in valid_positions:
        virtual_game_dict = dict(game_dict)
        virtual_valid_positions = list(valid_positions)
        virtual_game_dict[pos] = chance
        virtual_valid_positions.remove(pos)
        if chance == user_char:
            virtual_chance = comp_char
        else:
            virtual_chance = user_char
        if minormax == "max":
            virtual_minormax = "min"
        else:
            virtual_minormax = "max"
        result = check_game_status(virtual_game_dict)
        if result[0]:
            if result[1] == comp_char:
                scores.append(1)
            elif result[1] == user_char:
                scores.append(-1)
            else:
                scores.append(0)
            
        else:
            if not initial:
                if len(virtual_valid_positions):
                    scores.append(think(virtual_game_dict, virtual_valid_positions, virtual_chance, comp_char, user_char, False, virtual_minormax))
        if initial:
            if len(virtual_valid_positions):
                new_score = think(virtual_game_dict, virtual_valid_positions, virtual_chance, comp_char, user_char, False, virtual_minormax)
            else:
                new_score = scores[0]
            try:
                if minormax == "max":
                    if new_score > selected_position[1]:
                        selected_position = [pos, new_score]
                else:
                    if new_score < selected_position[1]:
                        selected_position = [pos, new_score]
            except:
                selected_position = [pos, new_score]
    if initial:
        return selected_position[0]
    if minormax == "max":
        score = max(scores) * scores.count(max(scores))
    elif minormax == "min":
        score = min(scores) * scores.count(min(scores))
    return score

def update_game(game_dict, pos, char):
    #this function takes the position selected by the user or computer and adds it to the game position-value dictionary with the value equal to the char provided
    #then it iterates through the ditionary and collects all the positions with value = " " (or empty) and adds them to valid positions
    #then it returns a list [game position-value dictionary, valid positions]
    game_dict[pos] = char
    valid_positions = []
    for key in list(game_dict.keys()):
        if game_dict[key] == " ":
            valid_positions.append(key)
    return [game_dict, valid_positions]

def check_game_status(game_dict):
    #this function takes the game position-value dictionary and checks if anyone (user or computer) has won the game, or the game is drawn or the game is not over yet.
    #if user wins the game, it returns a list [True, user character]
    #if computer wins the game, it returns a list [True, computer character]
    #if the game is a draw, it returns a list [True, " "]
    #if the game is not over yet, it returns a list [False]
    winning_case_list = [["11", "12", "13"], ["21", "22", "23"], ["31", "32", "33"], ["11", "21", "31"], ["12", "22", "32"], ["13" , "23", "33"], ["11", "22", "33"], ["13", "22", "31"]]
    is_draw = True
    for winning_case in winning_case_list:
        score = 0
        char = game_dict[winning_case[0]]
        if char != " ":
            for pos in winning_case:
                if game_dict[pos] == char:
                    score += 1
                elif game_dict[pos] == " ":
                    is_draw = False
            if score == 3:
                return [True, char]
        else:
            is_draw = False
    if is_draw:
        return [True, " "]
    else:
        return [False]

def start_game():
    #this is the main control of the game
    #reset the game position-value dictoinary
    game_dict = reset_game("game")
    #take the character from user with which the user wants to play the game
    user_char = take_user_input("Which character would you like to play with? [X/O]: ", ["X", "O"], "Please enter 'X' or 'O'")
    #as it is a new game all positions are vali. So put the valid_positions equal to the list of keys of game position-value dictionary
    valid_positions = list(game_dict.keys())
    #set the computer character according to the usr character
    if user_char == "X":
        comp_char = "O"
    else:
        comp_char = "X"
    #ask the user if he/she wants to play the first move
    user_starts = take_user_input("Would you like to play first move? [Y/N]: ", ["Y", "N"], "Please answer in 'Y' or 'N'")
    #set the chance according to user_starts
    if user_starts == "Y":
        chance = user_char
    else:
        chance = comp_char
    #the game starts here
    while True:
        if chance == user_char:
            #if it is user's chance, ask the user for position he wants to put his/her character
            pos = take_user_input("Enter the position you want to put " + chance + ": ", valid_positions + ['99'], "Please enter a valid position")
            if pos == '99':
                pos = think(game_dict, valid_positions, chance, user_char, comp_char, True, "max")
        else:
            #else, take the position from the think function, i.e., the computer
            print()
            print("Thinking...")
            pos = think(game_dict, valid_positions, chance, comp_char, user_char, True, "max")
            print("Computer Played: ",pos)
        #update the game position-value dictionary and the valid positions
        game = update_game(game_dict, pos, chance)
        #extracgt game position-value dicitonary and the valid positions from the game variable
        game_dict = game[0]
        valid_positions = game[1]
        #print the game
        print_game(game_dict)
        #check if anyonw won the game or it is a draw or the game is not over yet
        game_status = check_game_status(game_dict)
        if game_status[0]:
            #if someone won the game
            print()
            if game_status[1] == user_char:
                #if user won the game
                print("User won the game!")
            elif game_status[1] == comp_char:
                #if computer won the game
                print("Computer won the game!")
            else:
                #if the game was a draw
                print("The game was a draw!")
            print()
            #as the game has been completed, break the loop
            break
        else:
            #if the game is not over
            #change the chance according to its previous value
            if chance == user_char:
                #if it was user's chance, change it to computer's chance
                chance = comp_char
            else:
                #if it was computer's chance, change it to user's chance
                chance = user_char
    #after the game is over and the loop breaks, ask the user if he/she wants to play again, and return his/her answer
    play_again = take_user_input("Do you want to play again? [Y/N]: ", ["Y", "N"], "Please enter 'Y' or 'N'")
    return play_again

def main():
    #print the welcome note
    print("Welcome to TicTacToe!")
    print("Here you can see the position of every block, you need to enter the respective position to put your character in that block. For example, when asked, you should type '11' to put your character in the top-left block. Goodluck!")
    #reset the game position-value dictionary with mode = 'pos' in order to show the names of the positions to the user
    game_dict = reset_game("pos")
    #print the game
    print_game(game_dict)
    while True:
        #start_game() will start the game and return if the user wants to play again
        play_again = start_game()
        if play_again == "N":
            #if user doesn't want to play again, exit the game
            print("Thank you for playing")
            break
        #else the loop will continue and the game will start again

#call the main function
main()
