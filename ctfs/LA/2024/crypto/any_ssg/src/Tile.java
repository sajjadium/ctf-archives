public class Tile {

    private final String name;
    private final boolean filled;

    public Tile(String name) {
        this.name=name;
        filled = false;
    }

    public Tile(String name, boolean filled) {
        this.name = name;
        this.filled = filled;
    }

    public String getName() {
        return name;
    }
    public boolean getFilled() {
        return filled;
    }

}
