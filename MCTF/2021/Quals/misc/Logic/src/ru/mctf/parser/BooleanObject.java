package ru.mctf.parser;

public abstract class BooleanObject {

    private int id;
    private final BooleanObjectType type;
    private BooleanObject parent;

    protected BooleanObject(BooleanObjectType type) {
        this.type = type;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public BooleanObjectType getType() {
        return type;
    }

    public void setParent(BooleanObject parent) {
        this.parent = parent;
    }

    public BooleanObject getParent() {
        return parent;
    }

}
