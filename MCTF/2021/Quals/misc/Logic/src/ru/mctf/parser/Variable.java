package ru.mctf.parser;

public class Variable extends BooleanObject {

    private final String name;

    public Variable(String name) {
        super(BooleanObjectType.VARIABLE);
        this.name = name;
    }

    @Override
    public String toString() {
        return name;
    }

    public String getName() {
        return name;
    }
}
