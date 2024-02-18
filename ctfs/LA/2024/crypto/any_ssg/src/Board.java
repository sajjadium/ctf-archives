import java.lang.Math;
public class Board {

    private final int sizeX;
    private final int sizeY;
    private final Tile[][] tiles;
    private final Player player;
    public boolean completed;
    public boolean died;

    public Board(int x, int y) {
        sizeX = x;
        sizeY = y;
        tiles = new Tile[sizeX][sizeY];
        player = new Player();
        completed = false;
        died = false;
    }

    public int getSizeX() {
        return sizeX;
    }

    public int getSizeY() {
        return sizeY;
    }

    public Tile getTile(int x, int y) {
        return tiles[x][y];
    }

    public Player getPlayer() {
        return player;
    }

    public void setTile(int x, int y, Tile tile) {
        tiles[x][y] = tile;
    }

    public void movePlayer(int dx, int dy) {
        if ((0 <= player.getX() + dx) && (player.getX() + dx < sizeX)) {
            player.changeX(dx);
        }
        if ((0 <= player.getY() + dy) && (player.getY() + dy < sizeY)) {
            player.changeY(dy);
        }
        updatePlayer();
    }

    public void updatePlayer() {
        player.setCurrentTile(tiles[player.getX()][player.getY()]);
        if (player.getCurrentTile().getName().equals("end_portal")) {
            completed = true;
        }
        if (player.getCurrentTile().getName().equals("lava")) {
            died = true;
        }
    }

    public void generateStronghold(CustomRandom r) {
        boolean[] filledEyes = new boolean[16];
        int strongholdLocationX = Math.floorMod((int)r.nextLong(), sizeX-5);
        int strongholdLocationY = Math.floorMod((int)r.nextLong(), sizeY-5);
        boolean allFilled = true;
        for (int i = 0; i<16; i++) {
            long n = r.nextLong();
            if (n > (9 * (1L << 52)/10L)) {
                filledEyes[i] = true;
            }
            else {
                filledEyes[i] = false;
                allFilled = false;
            }
        }
        int n = 0;
        for (int i = 0; i< 4; i++) {
            Tile endPortal = new Tile("end_portal_frame",filledEyes[n]);
            setTile(strongholdLocationX+1+i,strongholdLocationY,endPortal);
            n++;
        }
        for (int i = 0; i< 4; i++) {
            Tile endPortal = new Tile("end_portal_frame",filledEyes[n]);
            setTile(strongholdLocationX,strongholdLocationY+1+i,endPortal);
            n++;
        }
        for (int i = 0; i< 4; i++) {
            Tile endPortal = new Tile("end_portal_frame",filledEyes[n]);
            setTile(strongholdLocationX+1+i,strongholdLocationY+5,endPortal);
            n++;
        }
        for (int i = 0; i< 4; i++) {
            Tile endPortal = new Tile("end_portal_frame",filledEyes[n]);
            setTile(strongholdLocationX+5,strongholdLocationY+1+i,endPortal);
            n++;
        }

        if (allFilled) {
            for (int i = 0; i<4; i++) {
                for (int j = 0; j<4; j++) {
                    setTile(strongholdLocationX+1+i,strongholdLocationY+1+j,new Tile("end_portal"));
                }
            }
        }
        else {
            for (int i = 0; i<4; i++) {
                for (int j = 0; j<4; j++) {
                    setTile(strongholdLocationX+1+i,strongholdLocationY+1+j,new Tile("lava"));
                }
            }
        }
    }

    public void generateCircle(CustomRandom r, Tile t) {
        int radius = Math.floorMod((int) r.nextLong(), 15);
        int circleX = Math.floorMod((int) r.nextLong(), sizeX);
        int circleY = Math.floorMod((int) r.nextLong(), sizeY);
        for (int i = circleX - radius; i<= circleX + radius; i++) {
            for (int j = circleY - radius; j<=circleY+radius; j++) {
                if (i >= 0 && i < sizeX && j >= 0 && j < sizeY && (Math.pow(i-circleX,2) + Math.pow(j-circleY,2))<=Math.pow(radius,2)) {
                    setTile(i,j,t);
                }
            }
        }
    }
}
