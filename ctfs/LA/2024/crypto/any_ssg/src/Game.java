public class Game {

    CustomRandom r = new CustomRandom();
    private final int sizeX = 50;
    private final int sizeY = 50;
    private final Board board;

    public Game(long seed) {
        r.setSeed(seed);
        board = new Board(sizeX,sizeY);
        generateBoard();
    }

    public Game() {
        board = new Board(sizeX,sizeY);
        generateBoard();
    }

    private void generateBoard(){
        for (int i = 0; i<sizeX; i++) {
            for (int j = 0; j<sizeY; j++) {
                board.setTile(i,j,new Tile("grass"));
            }
        }
        for (int i = 0; i<5; i++) {
            board.generateCircle(r,new Tile("stone"));
        }
        for (int i = 0; i<3; i++) {
            board.generateCircle(r,new Tile("water"));
        }
        board.generateStronghold(r);
        board.updatePlayer();
    }

    public void onW() {
        board.movePlayer(-1,0);
    }

    public void onS() {
        board.movePlayer(1,0);
    }

    public void onD() {
        board.movePlayer(0,1);
    }

    public void onA() {
        board.movePlayer(0,-1);
    }

    public Board getBoard() {
        return board;
    }
}
