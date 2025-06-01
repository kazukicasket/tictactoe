import random

boardSize = 3
lastRow, lastColumn, boardMiddle = boardSize - 1, boardSize - 1, int((boardSize - 1) / 2)
boardCharacter = "_"
playerSize = len(boardCharacter)
gameScore, sortedScore, lastScore, playerStats = {}, {}, {}, {}
gameMatches, victoryPoints, drawPoints, defeatPoints = 0, 3, 1, 0
bold_on, bold_off = "\033[1m", "\033[0m"


def random_move():
    global positionOne, positionTwo

    while True:
        positionOne, positionTwo = random.randrange(0, boardSize), random.randrange(0, boardSize)

        if gameBoard[positionOne][positionTwo] == boardCharacter:
            break


def smart_move():
    global positionOne, positionTwo

    if moveCounter == 0:
        positionOne, positionTwo = random.choice([0, lastRow]), random.choice([0, lastColumn])

    elif moveCounter == 1:
        if gameBoard[boardMiddle][boardMiddle] != boardCharacter:
            positionOne, positionTwo = random.choice([0, lastRow]), random.choice([0, lastColumn])

        else:
            if (gameBoard[0][0] != boardCharacter or gameBoard[0][lastColumn] != boardCharacter
                    or gameBoard[lastRow][0] != boardCharacter or gameBoard[lastRow][lastColumn] != boardCharacter):
                positionOne, positionTwo = boardMiddle, boardMiddle

            else:
                positionOne, positionTwo = random.choice([0, lastRow]), random.choice([0, lastColumn])

    else:
        diagonal_major_positions, diagonal_minor_positions = [], []
        diagonal_major_empty_positions, diagonal_minor_empty_positions = [], []
        priority_one, priority_two = False, False

        for i in range(boardSize):
            row_positions, column_positions = [], []
            row_empty_positions, column_empty_positions = [], []

            if gameBoard[i][lastRow - i] != boardCharacter:
                diagonal_minor_positions.append(gameBoard[i][lastRow - i])

            else:
                diagonal_minor_empty_positions.insert(0, (i, lastRow - i))

            for j in range(boardSize):
                if gameBoard[i][j] != boardCharacter:
                    row_positions.append(gameBoard[i][j])

                else:
                    row_empty_positions.insert(0, (i, j))

                if gameBoard[j][i] != boardCharacter:
                    column_positions.append(gameBoard[j][i])

                else:
                    column_empty_positions.insert(0, (j, i))

                if i == j:
                    if gameBoard[i][j] != boardCharacter:
                        diagonal_major_positions.append(gameBoard[i][j])

                    else:
                        diagonal_major_empty_positions.insert(0, (i, j))

            if len(row_positions) == 2:
                if row_positions.count(currentPlayer) == 2:
                    positionOne, positionTwo = row_empty_positions[0][0], row_empty_positions[0][1]
                    priority_one = True

                elif row_positions.count(nextPlayer) == 2 and not priority_one:
                    positionOne, positionTwo = row_empty_positions[0][0], row_empty_positions[0][1]
                    priority_two = True

            if len(column_positions) == 2:
                if column_positions.count(currentPlayer) == 2:
                    positionOne, positionTwo = column_empty_positions[0][0], column_empty_positions[0][1]
                    priority_one = True

                elif column_positions.count(nextPlayer) == 2 and not priority_one:
                    positionOne, positionTwo = column_empty_positions[0][0], column_empty_positions[0][1]
                    priority_two = True

            if not priority_one and not priority_two:
                if row_positions.count(currentPlayer) == 1 and len(row_positions) == 1:
                    temp_position = row_empty_positions[random.choice([0, 1])]
                    positionOne, positionTwo = temp_position[0], temp_position[1]

                elif column_positions.count(currentPlayer) == 1 and len(column_positions) == 1:
                    temp_position = column_empty_positions[random.choice([0, 1])]
                    positionOne, positionTwo = temp_position[0], temp_position[1]

        if len(diagonal_major_positions) == 2:
            if diagonal_major_positions.count(currentPlayer) == 2:
                positionOne, positionTwo = diagonal_major_empty_positions[0][0], diagonal_major_empty_positions[0][1]
                priority_one = True

            elif diagonal_major_positions.count(nextPlayer) == 2 and not priority_one:
                positionOne, positionTwo = diagonal_major_empty_positions[0][0], diagonal_major_empty_positions[0][1]
                priority_two = True

        if len(diagonal_minor_positions) == 2:
            if diagonal_minor_positions.count(currentPlayer) == 2:
                positionOne, positionTwo = diagonal_minor_empty_positions[0][0], diagonal_minor_empty_positions[0][1]
                priority_one = True

            elif diagonal_minor_positions.count(nextPlayer) == 2 and not priority_one:
                positionOne, positionTwo = diagonal_minor_empty_positions[0][0], diagonal_minor_empty_positions[0][1]
                priority_two = True

        if not priority_one and not priority_two:
            if diagonal_major_positions.count(currentPlayer) == 1 and len(diagonal_major_positions) == 1:
                temp_position = diagonal_major_empty_positions[random.choice([0, 1])]
                positionOne, positionTwo = temp_position[0], temp_position[1]

            elif diagonal_minor_positions.count(currentPlayer) == 1 and len(diagonal_minor_positions) == 1:
                temp_position = diagonal_minor_empty_positions[random.choice([0, 1])]
                positionOne, positionTwo = temp_position[0], temp_position[1]


def print_board():
    def default_print():
        if gameLayout == "1":
            if j == (boardSize - 1):
                print(f"{gameBoard[i][j]:^{playerSize + 2}}", end="")

            else:
                print(f"{gameBoard[i][j]:^{playerSize + 2}}|", end="")

        else:
            print(f"[{gameBoard[i][j]:^{playerSize + 2}}]", end="")

    for i in range(boardSize):
        for j in range(boardSize):
            if victoryMatch:
                if (i, j) in winningPositions:
                    if gameLayout == "1":
                        if j == (boardSize - 1):
                            print(f"*{gameBoard[i][j]:^{playerSize}}*", end="")

                        else:
                            print(f"*{gameBoard[i][j]:^{playerSize}}*|", end="")

                    else:
                        print(f"[*{gameBoard[i][j]:^{playerSize}}*]", end="")

                else:
                    default_print()

            else:
                if finishedMove:
                    if (i, j) == (positionOne, positionTwo):
                        if gameLayout == "1":
                            if j == (boardSize - 1):
                                print(f"{bold_on}{gameBoard[i][j]:^{playerSize + 2}}{bold_off}", end="")

                            else:
                                print(f"{bold_on}{gameBoard[i][j]:^{playerSize + 2}}{bold_off}|", end="")

                        else:
                            print(f"[{bold_on}{gameBoard[i][j]:^{playerSize + 2}}{bold_off}]", end="")

                    else:
                        default_print()

                else:
                    if (i, j) == (positionOne, positionTwo):
                        if gameLayout == "1":
                            if j == (boardSize - 1):
                                print(" * ", end="")

                            else:
                                print(" * |", end="")

                        else:
                            print("[ * ]", end="")

                    else:
                        default_print()

        print()


def set_ordinal(number):
    if number > 10:
        last_two_numbers = str(number)[-2] + str(number)[-1]

        if last_two_numbers == "11" or last_two_numbers == "12" or last_two_numbers == "13":
            return "th"

    if str(number)[-1] == "1":
        return "st"

    elif str(number)[-1] == "2":
        return "nd"

    elif str(number)[-1] == "3":
        return "rd"

    else:
        return "th"


def match_result():
    global winningPositions, victoryMatch, drawMatch

    diagonal_major_players, diagonal_minor_players = [], []
    diagonal_major_positions, diagonal_minor_positions = [], []

    for i in range(boardSize):
        row_players, column_players = [], []
        row_positions, column_positions = [], []

        if gameBoard[i][lastRow - i] == currentPlayer:
            diagonal_minor_players.append(currentPlayer)
            diagonal_minor_positions.insert(i, (i, lastRow - i))

        for j in range(boardSize):
            if gameBoard[i][j] == currentPlayer:
                row_players.append(currentPlayer)
                row_positions.insert(j, (i, j))

            if gameBoard[j][i] == currentPlayer:
                column_players.append(currentPlayer)
                column_positions.insert(j, (j, i))

            if i == j:
                if gameBoard[i][j] == currentPlayer:
                    diagonal_major_players.append(currentPlayer)
                    diagonal_major_positions.insert(j, (i, j))

        if row_players.count(currentPlayer) == 3:
            winningPositions = row_positions

        elif column_players.count(currentPlayer) == 3:
            winningPositions = column_positions

        elif diagonal_major_players.count(currentPlayer) == 3:
            winningPositions = diagonal_major_positions

        elif diagonal_minor_players.count(currentPlayer) == 3:
            winningPositions = diagonal_minor_positions

        if len(winningPositions) == 3:
            victoryMatch = True

        elif moveCounter >= 9:
            drawMatch = True


def sort_score(score):
    global sortedScore, lastScore

    if len(sortedScore) > 0:
        lastScore = sortedScore.copy()

    sortedScore.clear()
    temp_score = score.copy()
    key_player, rank_counter, equal_rank_counter = 0, 1, 0

    while len(sortedScore) != len(score):
        highest_score = 0
        temp_key_player = key_player

        for key in temp_score:
            if temp_score[key] >= highest_score:
                highest_score = temp_score[key]
                key_player = key

        if len(sortedScore) > 0:
            if highest_score not in sortedScore[temp_key_player].values():
                rank_counter += 1 + equal_rank_counter
                equal_rank_counter = 0

            else:
                equal_rank_counter += 1

        sortedScore[key_player] = {rank_counter: temp_score.pop(key_player)}

    for sorted_player in sortedScore:
        if sorted_player not in lastScore:
            lastScore[sorted_player] = "▶ "

        else:
            for last_rank in lastScore[sorted_player]:
                for sorted_rank in sortedScore[sorted_player]:
                    if sorted_rank < last_rank:
                        lastScore[sorted_player] = "▲ "

                    elif sorted_rank > last_rank:
                        lastScore[sorted_player] = "▼ "

                    elif sorted_rank == last_rank:
                        lastScore[sorted_player] = f"{bold_on}─{bold_off} "


def show_score(score):
    global playerStats

    sort_score(score)

    rank_digit_size, points_digit_size, matches_digit_size = 0, 0, 0
    wins_digit_size, draws_digit_size, defeats_digit_size = 0, 0, 0
    player_performance_100 = False

    for sorted_player in sortedScore:
        temp_matches = playerStats[sorted_player][0] + playerStats[sorted_player][1] + playerStats[sorted_player][2]

        if len(str(temp_matches)) > matches_digit_size:
            matches_digit_size = len(str(temp_matches))

        if len(str(playerStats[sorted_player][0])) > wins_digit_size:
            wins_digit_size = len(str(playerStats[sorted_player][0]))

        if len(str(playerStats[sorted_player][1])) > draws_digit_size:
            draws_digit_size = len(str(playerStats[sorted_player][1]))

        if len(str(playerStats[sorted_player][2])) > defeats_digit_size:
            defeats_digit_size = len(str(playerStats[sorted_player][2]))

        for sorted_rank in sortedScore[sorted_player]:
            if len(str(sorted_rank)) > rank_digit_size:
                rank_digit_size = len(str(sorted_rank))

            if len(str(sortedScore[sorted_player][sorted_rank])) > points_digit_size:
                points_digit_size = len(str(sortedScore[sorted_player][sorted_rank]))

            if (sortedScore[sorted_player][sorted_rank] /
                    ((temp_matches * victoryPoints) if temp_matches != 0 else 1) == 1.0):
                player_performance_100 = True

    print(f"\n{bold_on}>> SCORE <<{bold_off}")

    for sorted_player in sortedScore:
        for sorted_rank in sortedScore[sorted_player]:
            ordinal_rank = set_ordinal(sorted_rank)
            player_points = sortedScore[sorted_player][sorted_rank]
            player_wins = playerStats[sorted_player][0]
            player_draws = playerStats[sorted_player][1]
            player_defeats = playerStats[sorted_player][2]
            player_matches = player_wins + player_draws + player_defeats
            player_performance = (sortedScore[sorted_player][sorted_rank] /
                                  ((player_matches * victoryPoints) if player_matches != 0 else 1)) * 100

            print(f"{lastScore[sorted_player]}{bold_on}{sorted_rank:{rank_digit_size}}{ordinal_rank}.{bold_off} "
                  f"Player '{bold_on}{sorted_player}{bold_off}': ", end="")

            print(f"{player_points:{points_digit_size}} {'Points' if player_points > 1 else 'Point '} ", end="")

            print(f"{bold_on}|{bold_off} {player_matches:{matches_digit_size}} "
                  f"{'Matches' if player_matches > 1 else 'Match  '} ", end="")

            print(f"{bold_on}({bold_off}{player_wins:{wins_digit_size}} {'Wins' if player_wins > 1 else 'Win '} ",
                  end="")

            print(f"{bold_on}/{bold_off} {player_draws:{draws_digit_size}} {'Draws' if player_draws > 1 else 'Draw '} ",
                  end="")

            print(f"{bold_on}/{bold_off} {player_defeats:{defeats_digit_size}} "
                  f"{'Defeats' if player_defeats > 1 else 'Defeat '} ", end="")

            if not player_performance_100:
                print(f"{bold_on}~{bold_off} {player_performance:5.2f}%{bold_on}){bold_off}", end="")

            else:
                print(f"{bold_on}~{bold_off} {player_performance:6.2f}%{bold_on}){bold_off}", end="")

            if playerStats[sorted_player][3]:
                print(" *")

                playerStats[sorted_player][3] = 0

            else:
                print()

    if mainMenu != "7":
        input(f"\n{bold_on}Total Matches: {gameMatches}{bold_off}")

    else:
        print(f"\n{bold_on}Total Matches: {gameMatches}{bold_off}")


print(f"\n{bold_on}-T1C-TAC-T0E-{bold_off}")

while True:
    print(f"\n{bold_on}>> MAIN MENU <<{bold_off}\n"
          "1 - Game Modes\n"
          "2 - Score\n"
          "9 - Exit")
    mainMenu = input(f"{bold_on}Option:{bold_off} ").strip()

    if mainMenu == "1":
        playAgain, playerOne, playerTwo, currentPlayer, nextPlayer = "", "", "", "", ""
        enableMoveTips, enableMoveConfirmation, gameMode, gameLayout, robotLevel = "", "", "", "", ""
        positionOne, positionTwo = 0, 0

        while True:
            gameBoard = [[boardCharacter for j in range(boardSize)] for i in range(boardSize)]
            winningPositions = []
            exitCharacter, victoryMatch, drawMatch = False, False, False
            moveCounter = 0

            if playAgain != "1":
                print(f"\n{bold_on}>> GAME MODES <<{bold_off}\n"
                      "1 - Player vs Player\n"
                      "2 - Player vs AI\n"
                      "3 - AI vs AI\n"
                      "9 - Back")
                gameMode = input(f"{bold_on}Option:{bold_off} ").strip()

                if gameMode == "1" or gameMode == "2" or gameMode == "3":
                    while True:
                        if gameMode == "1":
                            print(f"\n{bold_on}>> PLAYER VS PLAYER <<{bold_off}\n")

                        elif gameMode == "2":
                            print(f"\n{bold_on}>> PLAYER VS AI <<{bold_off}\n")

                        elif gameMode == "3":
                            print(f"\n{bold_on}>> AI VS AI <<{bold_off}\n")

                        print(f"Enter {playerSize} Unique {'Character' if playerSize < 2 else 'Characters'} "
                              "to Represent Each Player:")
                        playerOne = input(f"{bold_on}Player One:{bold_off} ").upper().strip()
                        playerTwo = input(f"{bold_on}Player Two:{bold_off} ").upper().strip()

                        if playerOne == "9" and playerTwo == "9":
                            exitCharacter = True

                            break

                        if playerOne != playerTwo and playerOne != boardCharacter and playerTwo != boardCharacter:
                            if len(playerOne) == playerSize and len(playerTwo) == playerSize:
                                if playerOne not in gameScore:
                                    gameScore[playerOne] = 0
                                    playerStats[playerOne] = [0, 0, 0, 0]

                                if playerTwo not in gameScore:
                                    gameScore[playerTwo] = 0
                                    playerStats[playerTwo] = [0, 0, 0, 0]

                                currentPlayer = random.choice([playerOne, playerTwo])

                                if currentPlayer == playerOne:
                                    nextPlayer = playerTwo

                                else:
                                    nextPlayer = playerOne

                                if gameMode != "3":
                                    print(f"\nEnable {bold_on}Move Tips{bold_off}?\n"
                                          "0 - No\n"
                                          "1 - Yes")
                                    enableMoveTips = input(f"{bold_on}Option:{bold_off} ").strip()

                                    print(f"\nEnable {bold_on}Move Confirmation{bold_off}?\n"
                                          "0 - No\n"
                                          "1 - Yes")
                                    enableMoveConfirmation = input(f"{bold_on}Option:{bold_off} ").strip()

                                break

                            else:
                                input(f"\n{bold_on}ENTER EXACLY {playerSize} "
                                      f"{'CHARACTER' if playerSize < 2 else 'CHARACTERS'} FOR EACH PLAYER!{bold_off}")

                        else:
                            input(f"\n{bold_on}ENTER DIFFERENT CHARACTERS FOR EACH PLAYER!{bold_off}")

                elif gameMode == "9":
                    break

                else:
                    input(f"\n{bold_on}WRONG OPTION!{bold_off}")

                    exitCharacter = True

            if not exitCharacter:
                print(f"\n{bold_on}>> LAYOUT <<{bold_off}\n"
                      "1 - Classic X|Y\n"
                      "2 - Alternative [X][Y]")
                gameLayout = input(f"{bold_on}Option:{bold_off} ").strip()

                if gameMode != "1":
                    print(f"\n{bold_on}>> AI LEVEL <<{bold_off}\n"
                          "1 - Smart\n"
                          "2 - Dynamic\n"
                          "3 - Random")
                    robotLevel = input(f"{bold_on}Option:{bold_off} ").strip()

                while True:
                    random_move()

                    if gameMode == "1" or (gameMode == "2" and currentPlayer == playerOne):
                        moveTipConfirmation = ""
                        finishedMove = False

                        if enableMoveTips == "1":
                            print(f"\n{bold_on}>> PLAYER '{currentPlayer}' TURN <<{bold_off}\n")

                            print(f"Enable Move Tip for {bold_on}{moveCounter + 1}{set_ordinal(moveCounter + 1)}. "
                                  f"Move{bold_off}?\n"
                                  "0 - No\n"
                                  "1 - Yes")
                            tip_enabled = input(f"{bold_on}Option:{bold_off} ").strip()

                            if tip_enabled == "1":
                                smart_move()

                                if gameLayout == "1":
                                    print(f"\nSuggested Position: {bold_on}{positionOne}|{positionTwo}{bold_off}\n")

                                else:
                                    print(f"\nSuggested Position: {bold_on}[{positionOne}][{positionTwo}]{bold_off}\n")

                                print_board()

                                print(f"\n{bold_on}Confirm?{bold_off}\n"
                                      "0 - No\n"
                                      "1 - Yes")
                                moveTipConfirmation = input(f"{bold_on}Option:{bold_off} ").strip()

                        if moveTipConfirmation != "1":
                            while True:
                                while True:
                                    try:
                                        print(f"\nPlayer '{bold_on}{currentPlayer}{bold_off}' Move:")
                                        positionOne = int(input(f"{bold_on}{'|X|' if gameLayout == '1' else '[X]'} "
                                                                f"Coordinate:{bold_off} ").strip())
                                        positionTwo = int(input(f"{bold_on}{'|Y|' if gameLayout == '1' else '[Y]'} "
                                                                f"Coordinate:{bold_off} ").strip())

                                        break

                                    except ValueError:
                                        input(f"\n{bold_on}X AND Y MUST BE AN INTEGER!{bold_off}")

                                if 0 <= positionOne <= boardSize - 1 and 0 <= positionTwo <= boardSize - 1:
                                    if gameBoard[positionOne][positionTwo] == boardCharacter:
                                        if enableMoveConfirmation == "1":
                                            if gameLayout == "1":
                                                print(f"\nYour Move: {bold_on}{positionOne}|{positionTwo}{bold_off}\n")

                                            else:
                                                print(
                                                    f"\nYour Move: {bold_on}[{positionOne}][{positionTwo}]{bold_off}\n")

                                            print_board()

                                            print(f"\n{bold_on}Confirm?{bold_off}\n"
                                                  "0 - No\n"
                                                  "1 - Yes")
                                            move_confirmation = input(f"{bold_on}Option:{bold_off} ").strip()

                                            if move_confirmation == "1":
                                                break

                                        else:
                                            break

                                    else:
                                        if gameLayout == "1":
                                            input(f"\nTHE POSITION {bold_on}{positionOne}|{positionTwo}{bold_off} "
                                                  "IS NOT EMPTY!")

                                        else:
                                            input(f"\nTHE POSITION {bold_on}[{positionOne}][{positionTwo}]{bold_off} "
                                                  "IS NOT EMPTY!")

                                else:
                                    input(f"\n{bold_on}X AND Y MUST BE BETWEEN 0 AND {boardSize - 1}!{bold_off}")

                    else:
                        if robotLevel == "1":
                            smart_move()

                        elif robotLevel == "2":
                            print(f"\n{bold_on}>> PLAYER '{currentPlayer}' TURN <<{bold_off}\n"
                                  "1 - Smart Move\n"
                                  "2 - Random Move")
                            dynamic_option = input(f"{bold_on}Option:{bold_off} ").strip()

                            if dynamic_option == "1":
                                smart_move()

                            print()

                    if gameLayout == "1":
                        print(f"\nPlayer '{bold_on}{currentPlayer}{bold_off}' Move: {bold_on}{positionOne}|"
                              f"{positionTwo}{bold_off}")

                    else:
                        print(f"\nPlayer '{bold_on}{currentPlayer}{bold_off}' Move: {bold_on}[{positionOne}]"
                              f"[{positionTwo}]{bold_off}")

                    gameBoard[positionOne][positionTwo] = currentPlayer
                    finishedMove = True
                    moveCounter += 1

                    print(f"\n{bold_on}>> {moveCounter}{set_ordinal(moveCounter)}. MOVE <<{bold_off}\n")

                    match_result()
                    print_board()

                    if victoryMatch or drawMatch:
                        if victoryMatch:
                            gameScore[currentPlayer] += victoryPoints
                            playerStats[currentPlayer][0] += 1
                            playerStats[nextPlayer][2] += 1

                            input(f"\n{bold_on}>> VICTORY <<{bold_off}\n"
                                  f"{bold_on}* Player '{currentPlayer}' *{bold_off}\n"
                                  f"\nPlayer '{bold_on}{currentPlayer}{bold_off}': +{victoryPoints} Points\n"
                                  f"Player '{bold_on}{nextPlayer}{bold_off}': {'+' if defeatPoints >= 0 else ''}"
                                  f"{defeatPoints} {'Point' if abs(defeatPoints) < 2 else 'Points'}")

                        elif drawMatch:
                            gameScore[currentPlayer] += drawPoints
                            gameScore[nextPlayer] += drawPoints
                            playerStats[currentPlayer][1] += 1
                            playerStats[nextPlayer][1] += 1

                            input(f"\n{bold_on}>> DRAW <<{bold_off}\n"
                                  f"\nPlayer '{bold_on}{currentPlayer}{bold_off}': +{drawPoints} "
                                  f"{'Point' if drawPoints < 2 else 'Points'}\n"
                                  f"Player '{bold_on}{nextPlayer}{bold_off}': +{drawPoints} "
                                  f"{'Point' if drawPoints < 2 else 'Points'}")

                        gameMatches += 1
                        playerStats[currentPlayer][3] = 1
                        playerStats[nextPlayer][3] = 1

                        show_score(gameScore)

                        print(f"\nPlay Again with the {bold_on}Same Settings?{bold_off}\n"
                              "0 - No\n"
                              "1 - Yes")
                        playAgain = input(f"{bold_on}Option:{bold_off} ").strip()

                        break

                    if gameMode == "2":
                        if robotLevel != "2" and currentPlayer == playerOne:
                            input(f"\n{bold_on}ENTER TO CONTINUE{bold_off}")

                    elif gameMode == "3":
                        if robotLevel != "2":
                            input(f"\n{bold_on}ENTER TO CONTINUE{bold_off}")

                    if currentPlayer == playerOne:
                        currentPlayer = playerTwo
                        nextPlayer = playerOne

                    else:
                        currentPlayer = playerOne
                        nextPlayer = playerTwo

    elif mainMenu == "2":
        if len(gameScore) > 0:
            show_score(gameScore)

        else:
            input(f"\n{bold_on}NO REGISTERED PLAYERS!{bold_off}")

    elif mainMenu == "7":
        while True:
            print(f"\n{bold_on}>> GAMESHARK <<{bold_off}\n"
                  "0 - Reset Options\n"
                  "1 - Player Options\n"
                  "9 - Back")
            gameShark = input(f"{bold_on}Option:{bold_off} ").strip()

            if gameShark == "0":
                while True:
                    if len(gameScore) >= 1:
                        show_score(gameScore)

                    print(f"\n{bold_on}>> RESET OPTIONS <<{bold_off}\n"
                          "1 - Matches\n"
                          "2 - Players\n"
                          "9 - Back")
                    resetOption = input(f"{bold_on}Option:{bold_off} ").strip()

                    if resetOption == "1":
                        gameMatches = 0

                        for player_key in playerStats:
                            playerStats[player_key] = [0, 0, 0, 0]

                        for player_key in gameScore:
                            gameScore[player_key] = 0

                        input(f"\n{bold_on}MATCHES RESETED!{bold_off}")

                    elif resetOption == "2":
                        gameMatches = 0
                        gameScore.clear()
                        sortedScore.clear()
                        lastScore.clear()
                        playerStats.clear()

                        input(f"\n{bold_on}PLAYERS RESETED!{bold_off}")

                    elif resetOption == "9":
                        break

                    else:
                        input(f"\n{bold_on}WRONG OPTION!{bold_off}")

            elif gameShark == "1":
                while True:
                    if len(gameScore) >= 1:
                        show_score(gameScore)

                    print(f"\n{bold_on}>> PLAYER OPTIONS <<{bold_off}\n"
                          "1 - Add Player (Zero Stats)\n"
                          "2 - Add Player (Random Stats)\n"
                          "3 - Add Player (Custom Stats)\n"
                          "4 - Edit Player\n"
                          "5 - Remove Player\n"
                          "9 - Back")
                    playerOption = input(f"{bold_on}Option:{bold_off} ").strip()

                    if playerOption == "1" or playerOption == "2" or playerOption == "3":
                        while True:
                            print(f"\n{bold_on}>> ADD PLAYER <<{bold_off}\n"
                                  f"Enter {playerSize} {'Character' if playerSize < 2 else 'Characters'} "
                                  f"to Represent the Player:")
                            newPlayer = input(f"{bold_on}Player:{bold_off} ").upper().strip()

                            if newPlayer == "":
                                break

                            if len(newPlayer) == playerSize and newPlayer != boardCharacter:
                                if newPlayer not in gameScore:
                                    if playerOption == "1":
                                        gameScore[newPlayer] = 0
                                        playerStats[newPlayer] = [0, 0, 0, 1]

                                    elif playerOption == "2":
                                        newWins = random.randrange(0, random.choice([10, 100, 1000]))
                                        newDraws = random.randrange(0, random.choice([10, 100, 1000]))
                                        newDefeats = random.randrange(0, random.choice([10, 100, 1000]))
                                        gameScore[newPlayer] = (victoryPoints * newWins) + (drawPoints * newDraws)
                                        playerStats[newPlayer] = [newWins, newDraws, newDefeats, 1]

                                    elif playerOption == "3":
                                        while True:
                                            try:
                                                print(f"\n{bold_on}>> PLAYER '{newPlayer}' <<{bold_off}")

                                                newWins = int(input("Wins: ").strip())
                                                newDraws = int(input("Draws: ").strip())
                                                newDefeats = int(input("Defeats: ").strip())
                                                gameScore[newPlayer] = ((victoryPoints * newWins) +
                                                                        (drawPoints * newDraws))
                                                playerStats[newPlayer] = [newWins, newDraws, newDefeats, 1]

                                                break

                                            except ValueError:
                                                input(f"\n{bold_on}ENTER INTEGER NUMBERS!{bold_off}")

                                    break

                                else:
                                    input(f"\n{bold_on}PLAYER '{newPlayer}' ALREADY ADDED!{bold_off}")

                            else:
                                input(f"\n{bold_on}ENTER EXACLY {playerSize} "
                                      f"{'CHARACTER' if playerSize < 2 else 'CHARACTERS'} TO REPRESENT THE PLAYER!"
                                      f"{bold_off}")

                    elif playerOption == "4":
                        if len(gameScore) > 0:
                            while True:
                                print(f"\n{bold_on}>> EDIT PLAYER <<{bold_off}")

                                print("Enter the Player to Edit:")
                                editPlayer = input(f"{bold_on}Player:{bold_off} ").upper().strip()

                                if editPlayer == "":
                                    break

                                if editPlayer in gameScore:
                                    while True:
                                        try:
                                            print(f"\n{bold_on}>> PLAYER '{editPlayer}' <<{bold_off}")

                                            newWins = int(input("Wins: ").strip())
                                            newDraws = int(input("Draws: ").strip())
                                            newDefeats = int(input("Defeats: ").strip())
                                            gameScore[editPlayer] = (victoryPoints * newWins) + (drawPoints * newDraws)
                                            playerStats[editPlayer] = [newWins, newDraws, newDefeats, 1]

                                            break

                                        except ValueError:
                                            input(f"\n{bold_on}ENTER INTEGER NUMBERS!{bold_off}")

                                    break

                                else:
                                    input(f"\n{bold_on}PLAYER NOT FOUND!{bold_off}")

                        else:
                            input(f"\n{bold_on}NO REGISTERED PLAYERS!{bold_off}")

                    elif playerOption == "5":
                        if len(gameScore) > 0:
                            while True:
                                print(f"\n{bold_on}>> REMOVE PLAYER <<{bold_off}")

                                print("Enter the Player to Remove:")
                                removePlayer = input(f"{bold_on}Player:{bold_off} ").upper().strip()

                                if removePlayer == "":
                                    break

                                if removePlayer in gameScore:
                                    gameScore.pop(removePlayer)
                                    playerStats.pop(removePlayer)

                                    if removePlayer in sortedScore:
                                        sortedScore.pop(removePlayer)

                                    if removePlayer in lastScore:
                                        lastScore.pop(removePlayer)

                                    break

                                else:
                                    input(f"\n{bold_on}PLAYER NOT FOUND!{bold_off}")

                        else:
                            input(f"\n{bold_on}NO REGISTERED PLAYERS!{bold_off}")

                    elif playerOption == "9":
                        break

                    else:
                        input(f"\n{bold_on}WRONG OPTION!{bold_off}")

            elif gameShark == "9":
                break

            else:
                input(f"\n{bold_on}WRONG OPTION!{bold_off}")

    elif mainMenu == "9":
        break

    else:
        input(f"\n{bold_on}WRONG OPTION!{bold_off}")

print(f"\n{bold_on}>> THE END <<{bold_off}")
