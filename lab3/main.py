import chess
board = chess.Board()
print(board)

def evaluate(board, isWhiteMove):
    pawn = 100
    knight = 300
    bishop = 300
    rook = 500
    queen = 900
    king = 2500
    mobilityWeight = 10

    whitepawns = len(board.pieces(1, 1))
    whiteknights = len(board.pieces(2, 1))
    whitebishops = len(board.pieces(3, 1))
    whiterooks = len(board.pieces(4, 1))
    whitequeens = len(board.pieces(5, 1))
    whiteking = len(board.pieces(6, 1))
    whitematerial = pawn * whitepawns + knight * whiteknights + bishop * whitebishops + \
                    rook * whiterooks + queen * whitequeens + king * whiteking
    blackpawns = len(board.pieces(1, 0))
    blackknights = len(board.pieces(2, 0))
    blackbishops = len(board.pieces(3, 0))
    blackrooks = len(board.pieces(4, 0))
    blackqueens = len(board.pieces(5, 0))
    blackking = len(board.pieces(6, 0))
    blackmaterial = pawn * blackpawns + knight * blackknights + bishop * blackbishops + \
                    rook * blackrooks + queen * blackqueens + king * blackking
    material = whitematerial - blackmaterial

    mobility1 = len(list(board.legal_moves))

    board.push(chess.Move.null())
    mobility2 = len(list(board.legal_moves))
    board.pop()
    mobility = mobilityWeight * (mobility1 - mobility2)
    if (board.turn != isWhiteMove):
        mobility = -mobility

    if not isWhiteMove:
        return - material + mobility
    else:
        return material + mobility

def getListOfMoves(board, otherSide=False):
    moves = None
    if otherSide:
        board.push(chess.Move.null())
        moves = list(map(str, list(board.legal_moves)))
        board.pop()
    else:
        moves = list(map(str, list(board.legal_moves)))
    return moves


def getMoveWithNegaMax(board, depth):
    def negaMax(board1, depth1):
        if depth1 == 0:
            return evaluate(board1, board1.turn)
        maxValue1 = - 1_000_000
        for move1 in getListOfMoves(board1):
            boardCopy1 = board1.copy()
            boardCopy1.push_uci(move1)
            value1 = -negaMax(boardCopy1, depth1 - 1)
            if value1 > maxValue1:
                maxValue1 = value1
        return maxValue1

    maxValue = -1_000_000
    bestMove = None
    for move in getListOfMoves(board):
        boardCopy = board.copy()
        boardCopy.push_uci(move)
        value = -negaMax(boardCopy, depth)
        if value > maxValue:
            maxValue = value
            bestMove = move
    return bestMove


def getMoveWithNegaScout(board, depth):
    def negaScout(board1, depth1, alpha, beta):
        if depth1 == 0:
            return evaluate(board1, board1.turn)
        low = -1_000_000
        high = beta
        for move1 in getListOfMoves(board1):
            boardCopy1 = board1.copy()
            boardCopy1.push_uci(move1)
            value1 = -negaScout(boardCopy1, depth1 - 1, -high, -max(alpha, low))
            if value1 > low:
                if (high == beta or depth1 < 3 or value1 >= beta):
                    low = value1
                else:
                    low = -negaScout(boardCopy1, depth1 - 1, -beta, -value1)
            if low >= beta:
                return low
            high = max(alpha, low) + 1
        return low

    maxValue = -1_000_000
    bestMove = None
    for move in getListOfMoves(board):
        boardCopy = board.copy()
        boardCopy.push_uci(move)
        value = -negaScout(boardCopy, depth, -1_000_000, 1_000_000)
        if value > maxValue:
            maxValue = value
            bestMove = move
    return bestMove


def getMoveWithPVS(board, depth):
    def PVS(board1, depth1, alpha, beta):
        if depth1 == 0:
            return evaluate(board1, board1.turn)
        low = -1_000_000
        high = beta
        for move1 in getListOfMoves(board1):
            boardCopy1 = board1.copy()
            boardCopy1.push_uci(move1)
            value1 = -PVS(boardCopy1, depth1 - 1, -high, -max(alpha, low))
            if value1 > low:
                low = -PVS(boardCopy1, depth1 - 1, -beta, -alpha)
            if low >= beta:
                return low
            high = max(alpha, low) + 1
        return low

    maxValue = -1_000_000
    bestMove = None
    for move in getListOfMoves(board):
        boardCopy = board.copy()
        boardCopy.push_uci(move)
        value = -PVS(boardCopy, depth, -1_000_000, 1_000_000)
        if value > maxValue:
            maxValue = value
            bestMove = move
    return bestMove

board = chess.Board()

for i in range(10):
    move = getMoveWithNegaMax(board, 2)
    #move = getMoveWithNegaScout(board, 2)
    #move = getMoveWithPVS(board, 2)
    if not i % 2:
        print("White: ", move)
    else:
        print("Black: ", move)
    board.push_uci(move)

print(board)

