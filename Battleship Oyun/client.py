import socket
import json
import os
import random
 
# Constants
HOST = '192.168.142.76'
PORT = 12345
BOARD_SIZE = 10
EMPTY = '.'
SHIP = 'o'
HIT = 'x'
MISS = 'm'
 
SHIPS = {
    '4': 1,
    '3': 2,
    '2': 3,
    '1': 4,
}
 
def empty_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
 
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
 
def print_board(board, title):
    charA = 65
    print(title)
    print('    1 2 3 4 5 6 7 8 9 10')
    print()
    for row in board:
        print(chr(charA) + '   ', end='')
        print(' '.join(row))
        charA += 1
    print()
 
def is_valid_placement(board, row, col, length, direction):
    """Check if the ship can be placed on the board at the specified location and direction."""
    if direction == 'H':
        if col + length > BOARD_SIZE:
            return False
        for i in range(length):
            if board[row][col + i] != EMPTY:
                return False
    else:  # direction == 'V'
        if row + length > BOARD_SIZE:
            return False
        for i in range(length):
            if board[row + i][col] != EMPTY:
                return False
    return True
 
def place_ship(board, row, col, length, direction):
    """Place the ship on the board."""
    if direction == 'H':
        for i in range(length):
            board[row][col + i] = SHIP
    else:  # direction == 'V'
        for i in range(length):
            board[row + i][col] = SHIP
 
def add_ships_to_board(board, ships):
    """Add all ships to the board."""
    for length, count in ships.items():
        length = int(length)
        for _ in range(count):
            placed = False
            while not placed:
                direction = random.choice(['H', 'V'])
                row = random.randint(0, BOARD_SIZE - 1)
                col = random.randint(0, BOARD_SIZE - 1)
                if is_valid_placement(board, row, col, length, direction):
                    place_ship(board, row, col, length, direction)
                    placed = True
 
def create_board():
    """Create a board with ships placed randomly."""
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    add_ships_to_board(board, SHIPS)
    return board
 
def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Create initial board with ships
        board = create_board()
        sock.sendto(json.dumps(board).encode('utf-8'), (HOST, PORT))
 
        # Receive player ID from server
        player_id, _ = sock.recvfrom(4096)
        player_id = int(player_id.decode('utf-8'))
        print(f'Connected to the server as Player {player_id}')
 
        # Initialize opponent board to track hits and misses
        opponent_board = empty_board()
 
        while True:
            # Wait for server message
            msg, _ = sock.recvfrom(4096)
            msg = msg.decode('utf-8')
 
            if msg == 'YOUR_TURN':
                # Display boards
                clear_console()
                print_board(board, 'Your board:')
                print_board(opponent_board, 'Opponent board:')
 
                # It's this player's turn
                print('Your turn! Enter your move (e.g., A5):')
                move = input().strip()
                row = ord(move[0].upper()) - 65
                col = int(move[1:]) - 1
 
                # Send move data along with player ID to the server
                data = {
                    'player_id': player_id,
                    'move': {'row': row, 'col': col}
                }
                sock.sendto(json.dumps(data).encode('utf-8'), (HOST, PORT))
 
                # Receive the result
                result, _ = sock.recvfrom(4096)
                result = result.decode('utf-8')
                print(f'Result of your move: {result}')
                
                if result == 'HIT':
                    opponent_board[row][col] = HIT
                    clear_console()
                    print_board(board, 'Your board:')
                    print_board(opponent_board, 'Opponent board:')
                else:
                    if opponent_board[row][col] != HIT:  # Check if it wasn't a hit before marking as a miss
                        opponent_board[row][col] = MISS
 
            elif msg == 'WAIT':
                # It's the opponent's turn
                print('Waiting for the opponent...')
            else:
                # Update both boards with hits and misses
                update = json.loads(msg)
                move = update['move']
                result = update['result']
                if update['player_id'] != player_id:  # if move was not by this player
                    if result == 'HIT':
                        board[move['row']][move['col']] = HIT
                    else:
                        board[move['row']][move['col']] = MISS
 
                clear_console()
                print_board(board, 'Your board:')
                print_board(opponent_board, 'Opponent board:')
                print('Waiting for the opponent...')
 
start_client()