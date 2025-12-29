import pygame
import random

# 1. 오디오 초기화 예외 처리
try:
    pygame.mixer.init()
    HAS_AUDIO = True
except pygame.error:
    HAS_AUDIO = False
    print("오디오 장치를 찾을 수 없어 무음 모드로 실행합니다.")

# 설정값
CELL_SIZE = 30
COLUMNS = 10
ROWS = 20
WIDTH = CELL_SIZE * (COLUMNS + 6)
HEIGHT = CELL_SIZE * ROWS
FPS = 30

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128),
    (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)
]

# 테트리스 모양 정의
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[0, 1, 0], [1, 1, 1]], # T
    [[0, 1, 1], [1, 1, 0]], # S
    [[1, 1, 0], [0, 1, 1]], # Z
    [[1, 0, 0], [1, 1, 1]], # J
    [[0, 0, 1], [1, 1, 1]]  # L
]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Python Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.score = 0
        self.game_over = False
        
        # 배경 음악 재생
        if HAS_AUDIO:
            try:
                pygame.mixer.music.load("music.mp3") 
                pygame.mixer.music.play(-1)
            except:
                print("music.mp3 파일이 없어 음악을 재생하지 않습니다.")

        self.next_piece = self.get_random_piece()
        self.new_piece()

    def get_random_piece(self):
        idx = random.randint(0, len(SHAPES) - 1)
        return {"shape": SHAPES[idx], "color": COLORS[idx]}

    def new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = self.get_random_piece()
        # 중앙 배치 계산 수정: self.current_piece['shape'][0] 사용
        self.p_x = COLUMNS // 2 - len(self.current_piece['shape'][0]) // 2
        self.p_y = 0

        if self.check_collision(self.p_x, self.p_y, self.current_piece['shape']):
            self.game_over = True

    def rotate(self, shape):
        return [list(row) for row in zip(*shape[::-1])]

    def check_collision(self, x, y, shape):
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    if (x + c < 0 or x + c >= COLUMNS or 
                        y + r >= ROWS or self.grid[y + r][x + c]):
                        return True
        return False

    def lock_piece(self):
        for r, row in enumerate(self.current_piece['shape']):
            for c, cell in enumerate(row):
                if cell:
                    self.grid[self.p_y + r][self.p_x + c] = self.current_piece['color']
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        new_grid = [row for row in self.grid if not all(row)]
        lines_cleared = ROWS - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(COLUMNS)])
        self.grid = new_grid
        self.score += lines_cleared * 100

    def draw(self):
        self.screen.fill(BLACK)
        
        # 쌓인 블록 그리기
        for r in range(ROWS):
            for c in range(COLUMNS):
                if self.grid[r][c]:
                    pygame.draw.rect(self.screen, self.grid[r][c], (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))

        # 현재 블록 그리기
        for r, row in enumerate(self.current_piece['shape']):
            for c, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.current_piece['color'], 
                                   ((self.p_x + c)*CELL_SIZE, (self.p_y + r)*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))

        # UI 영역
        font = pygame.font.SysFont('malgungothic', 20) # 한글 폰트 없을 시 기본 폰트로 대체됨
        
        # Next 미리보기 (왼쪽 상단)
        self.screen.blit(font.render("Next:", True, WHITE), (WIDTH - 150, 50))
        for r, row in enumerate(self.next_piece['shape']):
            for c, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.next_piece['color'], (WIDTH - 150 + c*20, 80 + r*20, 18, 18))

        # 점수 (오른쪽 상단 근처)
        score_txt = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_txt, (WIDTH - 150, 150))

        pygame.display.flip()

    def run(self):
        drop_time = 0
        while not self.game_over:
            dt = self.clock.tick(FPS)
            drop_time += dt

            if drop_time > 500:
                if not self.check_collision(self.p_x, self.p_y + 1, self.current_piece['shape']):
                    self.p_y += 1
                else:
                    self.lock_piece()
                drop_time = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if not self.check_collision(self.p_x - 1, self.p_y, self.current_piece['shape']):
                            self.p_x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if not self.check_collision(self.p_x + 1, self.p_y, self.current_piece['shape']):
                            self.p_x += 1
                    elif event.key == pygame.K_DOWN:
                        if not self.check_collision(self.p_x, self.p_y + 1, self.current_piece['shape']):
                            self.p_y += 1
                    elif event.key == pygame.K_UP:
                        rotated = self.rotate(self.current_piece['shape'])
                        if not self.check_collision(self.p_x, self.p_y, rotated):
                            self.current_piece['shape'] = rotated
                    elif event.key == pygame.K_SPACE:
                        while not self.check_collision(self.p_x, self.p_y + 1, self.current_piece['shape']):
                            self.p_y += 1
                        self.lock_piece()
            self.draw()

        print(f"게임 오버! 최종 점수: {self.score}")
        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()