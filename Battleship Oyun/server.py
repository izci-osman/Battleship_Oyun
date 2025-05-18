import socket
import json
import threading
 
# Constants
HOST = '192.168.142.105'
PORT = 12345
BOARD_SIZE = 10
EMPTY = '.'
SHIP = 'o'
HIT = 'x'
MISS = 'm'
 
# Initialize game state
player_boards = [None, None]
player_addresses = [None, None]
player_turn = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
 
def handle_client(player_id, player_addresses, player_boards):
    global player_turn
    while True:
        data, addr = sock.recvfrom(4096)
        print(data, addr)
        print(player_id, player_turn)
        print(threading.active_count())
        
        # Check if the message is from the expected player
        if addr == player_addresses[player_turn]:
            # Decode the message
            move_data = json.loads(data.decode('utf-8'))
            received_player_id = move_data['player_id']
            move = move_data['move']
            
            # Check if the received player ID matches the expected player ID
            if received_player_id == player_id:
                row, col = move['row'], move['col']
 
                opponent_id = 1 - player_id
                if player_boards[opponent_id][row][col] == SHIP:
                    player_boards[opponent_id][row][col] = HIT
                    result = 'HIT'
                else:
                    result = 'MISS'
                
                sock.sendto(result.encode('utf-8'), addr)
                
                # Construct the response data
                response_data = {
                    'move': move,
                    'result': result,
                    'player_id': player_id,
                    'next_turn': player_turn if (result == 'HIT' and received_player_id == player_turn) else opponent_id
                }
                
                # Send the response to both players
                for i, addr in enumerate(player_addresses):
                    sock.sendto(json.dumps(response_data).encode('utf-8'), addr)
 
                # Switch turns only if it was a miss or if it was a hit and the same player gets another turn
                if result == 'MISS' or (result == 'HIT' and received_player_id == player_turn):
                    player_turn = opponent_id
 
                # Notify the players whose turn it is
                for i, player_addr in enumerate(player_addresses):
                    if i == player_turn:
                        sock.sendto(b'YOUR_TURN', player_addr)
                    else:
                        sock.sendto(b'WAIT', player_addr)
            else:
                print(f"Received message from unexpected player {received_player_id} instead of player {player_turn}")
 
def start_server():
    global player_turn
    print('Server started, waiting for players to connect...')
 
    # Wait for initial boards from both players
    for i in range(2):
        data, addr = sock.recvfrom(4096)
        player_addresses[i] = addr
        player_boards[i] = json.loads(data.decode('utf-8'))
        sock.sendto(str(i).encode('utf-8'), addr)
 
    print('Both players connected. Starting the game.')
 
    # Notify the first player that it's their turn
    sock.sendto(b'YOUR_TURN', player_addresses[player_turn])
    sock.sendto(b'WAIT', player_addresses[1 - player_turn])
 
    # Start a thread to handle each player
    for i in range(2):
        threading.Thread(target=handle_client, args=(i,player_addresses, player_boards)).start()
 
start_server()