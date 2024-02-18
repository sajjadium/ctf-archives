public class Player {

    private int x;
    private int y;
    private Tile currentTile;

    public Player() {
        x = 0;
        y = 0;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public Tile getCurrentTile() {
        return currentTile;
    }

    public void changeX(int d) {
        x+=d;
    }

    public void changeY(int d) {
        y+=d;
    }

    public void setCurrentTile(Tile t) {
        currentTile=t;
    }

}
