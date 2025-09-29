import sys, socket, json, threading, queue, time
import pygame

WIDTH, HEIGHT = 900, 600
BG = (8, 10, 16)
FG = (230, 235, 240)
TRACK_CLR = (40, 40, 48)
FINISH_CLR = (220, 220, 220)
ROVER_CLR = (120, 200, 255)
OBST_CLR = (255, 120, 120)
PX_PER_WU = 2.2

class Net:
    def __init__(self, host, port):
        self.sock = socket.create_connection((host, port))
        self.r = self.sock.makefile('r', buffering=1, encoding='utf-8', newline='\n')
        self.q = queue.Queue()
        self.alive = True
        threading.Thread(target=self.reader, daemon=True).start()
    def reader(self):
        try:
            for line in self.r:
                line = line.strip()
                if not line:
                    continue
                try:
                    self.q.put(json.loads(line))
                except Exception:
                    pass
        except Exception:
            pass
        self.alive = False

def world_to_screen_x(x_wu, half_width_wu, rover_x=0.0):
    left = WIDTH * 0.2
    right = WIDTH * 0.8
    x_rel = float(x_wu) - float(rover_x)
    t = (x_rel + half_width_wu) / (2 * half_width_wu)
    return int(left + t * (right - left))

def main():
    if len(sys.argv) != 3:
        print(f"usage: python {sys.argv[0]} HOST PORT")
        sys.exit(1)
    host, port = sys.argv[1], int(sys.argv[2])

    net = Net(host, port)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Race: Rover")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)
    big = pygame.font.SysFont(None, 48)

    latest = None
    flag = None
    flag_time = None

    while True:
        try:
            while True:
                obj = net.q.get_nowait()
                if obj.get("t") == "telemetry":
                    latest = obj
                    if obj.get("flag") is not None and flag is None:
                        flag = obj["flag"]
                        flag_time = time.time()
        except queue.Empty:
            pass
        '''
        
        TODO: Implement the controls for the rover client!

        {"t":"can","frame":"0123456789abcdef"}
        
        '''
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); return
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit(); return
                elif e.key == pygame.K_UP:
                    pass
                elif e.key == pygame.K_DOWN:
                    pass
                elif e.key == pygame.K_LEFT:
                    pass
                elif e.key == pygame.K_RIGHT:
                    pass
                elif e.key == pygame.K_b:
                    pass
                elif e.key == pygame.K_s:
                    pass
                elif e.key == pygame.K_r:
                    pass

        screen.fill(BG)

        if latest:
            track = latest.get("track", {})
            half_w = float(track.get("half_width", 60.0))
            rover_x = float(latest.get("x", 0.0))
            tlx = world_to_screen_x(-half_w, half_w, rover_x)
            trx = world_to_screen_x(+half_w, half_w, rover_x)
            track_px_w = max(1, trx - tlx)
            pygame.draw.rect(screen, TRACK_CLR, (tlx, 0, track_px_w, HEIGHT), border_radius=12)

            s = float(latest.get("s", 0.0))
            length = float(track.get("length", 1.0))
            progress = s / max(1.0, length)
            if progress > 0.85:
                for y in range(0, HEIGHT, 14):
                    pygame.draw.line(screen, FINISH_CLR, (trx, y), (trx, y+7), 3)

            obs = latest.get("obstacles", [])
            if obs is not None:
                for ob in obs:
                    try:
                        dy = float(ob["dy"])
                        if dy < 0:
                            continue
                        y = int(HEIGHT/2 - dy * PX_PER_WU)
                        x = world_to_screen_x(float(ob["x"]), half_w, rover_x)
                        w_px = max(6, int((float(ob["w"]) / (2 * half_w)) * track_px_w))
                        rect = pygame.Rect(x - w_px//2, y - 10, w_px, 20)
                        pygame.draw.rect(screen, OBST_CLR, rect, border_radius=4)
                    except (KeyError, ValueError, TypeError):
                        continue

            rover_rect = pygame.Rect(WIDTH//2 - 16, HEIGHT//2 + 18, 32, 44)
            pygame.draw.rect(screen, ROVER_CLR, rover_rect, border_radius=6)
            pygame.draw.rect(screen, FG, rover_rect, 2, border_radius=6)

            hud = [
                f"Status: {latest.get('status','')}",
                f"Dist: {s:.1f}/{length:.0f} wu",
                f"Lateral x: {rover_x:.1f} wu",
                f"Speed: {float(latest.get('vel',0.0)):.2f} wu/s",
                f"Throttle: {latest.get('throttle_pct',0)}%  Steer: {latest.get('steer_pct',0)}%",
                f"{str(latest.get('msg',''))[:64]}",
            ]
            for i, line in enumerate(hud):
                img = font.render(line, True, FG)
                screen.blit(img, (12, 10 + i*18))

        if flag:
            img = big.render(flag, True, (255, 240, 120))
            screen.blit(img, img.get_rect(center=(WIDTH//2, HEIGHT//2 - 80)))
            if time.time() - flag_time > 6:
                pygame.quit(); return

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
