import pygame
import sys
import random

board = [['' for _ in range(3)] for _ in range(3)]

def make_move(row, col, current,board):
    board[row][col] = current

def check_winner():
    # 행, 열, 대각선 검사
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != '':
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

def is_board_full():
    for row in board:
        if '' in row:
            return False
    return True

def level1(board):
    # 가능한 모든 빈 칸의 위치를 찾습니다.
    available_positions = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    # 가능한 위치 중에서 랜덤하게 선택합니다.
    row, col = random.choice(available_positions)
    return row, col

def create_random_weight():
    weight=[[random.uniform(0,1) for i in range(3)] for j in range(3)]
    weightsum=sum(sum(row) for row in weight)
    result_weight = [[element/weightsum for element in row] for row in weight]
    return result_weight
draw=0
notdraw=0
def average_weights(weight0, weight1):
    average = [[(weight0[row][col] + weight1[row][col]) / 2 for col in range(3)] for row in range(3)]
    return average

def playTTTself_noob(weight0, weight1,current,board):
    current_weight = weight0 if current == 'O' else weight1
    best_score = -1
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                if current_weight[row][col] > best_score:
                    best_score = current_weight[row][col]
                    best_move = (row, col)

    if best_move:
        make_move(best_move[0], best_move[1], current,board)
        winner = check_winner()
        if winner:
            global notdraw
            notdraw+=1
            return weight0 if winner == 'O' else weight1
        else:
            next_player = 'X' if current == 'O' else 'O'
            return playTTTself_noob(weight0, weight1, next_player,board)
    else:
        global draw
        draw+=1
        return average_weights(weight0, weight1)

def train_noob(): # can't training. Cause random computer almost always draw
    weight10240=[[create_random_weight() for k in range(1024)] for l in range(10)]
    for l in range(0,10):
        k=1024
        while(k>0):
            k//=2
            for j in range (0,k):
                board = [['' for _ in range(3)] for _ in range(3)]
                weight10240[l][j]=average_weights(playTTTself_noob(weight10240[l][2*j],weight10240[l][2*j+1],'O',board),
                                                  playTTTself_noob(weight10240[l][2*j+1],weight10240[l][2*j],'O',board))
    weight=[[0 for i in range(3)] for j in range(3)]
    for i in range(3):
        for j in range(3):
            for l in range(10):
                weight[i][j]+=weight10240[l][0][i][j]
            weight[i][j]/=10
    return weight
        

print(train_noob())
"""
weight0=[[1,100,1],[1,100,1],[1,100,1]]
weight1=[[1,1,100],[1,1,100],[1,1,100]]
board = [['' for _ in range(3)] for _ in range(3)]
print(playTTTself_noob(weight0, weight1,'O',board))
print(playTTTself_noob(weight1, weight0,'O',board))
"""
print(draw)
print(notdraw)

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# 파이게임 초기화
pygame.init()

# 화면 크기 설정
allsize=1000
size = 600
cell_size = size // 3
screen = pygame.display.set_mode((allsize, size))
pygame.display.set_caption('Tic Tac Toe')

# 게임 보드 초기화
board = [['' for _ in range(3)] for _ in range(3)]
current_player = 'O'
game_over = False

# 글꼴 설정
font = pygame.font.Font(None, 200)
small_font = pygame.font.Font(None, 40)

def draw_board():
    screen.fill(WHITE)
    # 수직선 그리기
    pygame.draw.line(screen, BLACK, (cell_size, 0), (cell_size, size), 3)
    pygame.draw.line(screen, BLACK, (2 * cell_size, 0), (2 * cell_size, size), 3)
    pygame.draw.line(screen, BLACK, (3 * cell_size, 0), (3 * cell_size, size), 3)
    # 수평선 그리기
    pygame.draw.line(screen, BLACK, (0, cell_size), (size, cell_size), 3)
    pygame.draw.line(screen, BLACK, (0, 2 * cell_size), (size, 2 * cell_size), 3)

    for row in range(3):
        for col in range(3):
            if board[row][col] != '':
                text = font.render(board[row][col], True, RED if board[row][col] == 'X' else BLUE)
                screen.blit(text, (col * cell_size + 30, row * cell_size + 10))

def selectfirst():
    screen.fill(WHITE)
    # 게임 제목 표시
    title_text = small_font.render("Tic Tac Toe", True, BLACK)
    title_rect = title_text.get_rect(center=(size // 2, 100))
    screen.blit(title_text, title_rect)
    # 누가 먼저 시작할지 안내 문구 표시
    who_first_text = small_font.render("Who goes first?", True, BLACK)
    who_first_rect = who_first_text.get_rect(center=(size // 2, 200))
    screen.blit(who_first_text, who_first_rect)
    # 사용자 또는 컴퓨터 선택 안내 문구 표시
    user_text = small_font.render("Press U for User", True, BLACK)
    user_rect = user_text.get_rect(center=(size // 2, 300))
    screen.blit(user_text, user_rect)
    comp_text = small_font.render("Press C for Computer", True, BLACK)
    comp_rect = comp_text.get_rect(center=(size // 2, 350))
    screen.blit(comp_text, comp_rect)

def selectplayer():
    screen.fill(WHITE)
    # 게임 제목 표시
    title_text = small_font.render("Tic Tac Toe", True, BLACK)
    title_rect = title_text.get_rect(center=(size // 2, 100))
    screen.blit(title_text, title_rect)
    # 플레이어 수를 묻는 질문
    who_first_text = small_font.render("How many players?", True, BLACK)
    who_first_rect = who_first_text.get_rect(center=(size // 2, 200))
    screen.blit(who_first_text, who_first_rect)
    # 1명 또는 2명
    user_text = small_font.render("Press 1 for vs computer", True, BLACK)
    user_rect = user_text.get_rect(center=(size // 2, 300))
    screen.blit(user_text, user_rect)
    comp_text = small_font.render("Press 2 for 2Players", True, BLACK)
    comp_rect = comp_text.get_rect(center=(size // 2, 350))
    screen.blit(comp_text, comp_rect)

player=0
while player==0:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                player=1
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                player=2
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    selectplayer()
    pygame.display.flip()

user_choice = ''
while user_choice not in ['U', 'C'] and player==1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                user_choice = 'U'
            elif event.key == pygame.K_c:
                user_choice = 'C'
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    selectfirst()
    pygame.display.flip()

board = [['' for _ in range(3)] for _ in range(3)]
if user_choice == 'C':
    current_player = 'X'
else:
    current_player = 'O'
game_over = False


def reset_game():
    global board, current_player, game_over
    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = 'O'
    game_over = False

# 게임 루프
while True:
    if(player==1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_player == 'O':
                x, y = event.pos
                col = x // cell_size
                row = y // cell_size
                if(col>=3):
                    continue
                if board[row][col] == '':
                    board[row][col] = current_player
                    winner = check_winner()
                    if winner:
                        game_over = True
                    elif is_board_full():
                        game_over = True
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'
            # 컴퓨터가 수를 둘 차례
            if not game_over and current_player == 'X':
                available_positions = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
                row, col = level1(board)
                board[row][col] = current_player
                winner = check_winner()
                if winner:
                    game_over = True
                elif is_board_full():
                    game_over = True
                else:
                    current_player = 'X' if current_player == 'O' else 'O'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                if event.key == pygame.K_q:
                    exit()
    else:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    x, y = event.pos
                    col = x // cell_size
                    row = y // cell_size
                    if(col>=3):
                        continue
                    if board[row][col] == '':
                        board[row][col] = current_player
                        winner = check_winner()
                        if winner:
                            game_over = True
                        elif is_board_full():
                            game_over = True
                        else:
                            current_player = 'O' if current_player == 'X' else 'X'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                



    draw_board()
    if game_over:
        winner = check_winner()
        if winner:
            text = small_font.render(f'{winner} wins! Press R to restart, Press Q to exit', True, BLACK)
        else:
            text = small_font.render('Draw! Press R to restart, Press Q to exit', True, BLACK)
        screen.blit(text, (20, size // 2 - 20))

    pygame.display.flip()
