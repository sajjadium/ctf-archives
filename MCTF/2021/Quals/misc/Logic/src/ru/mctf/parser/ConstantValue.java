package ru.mctf.parser;

public class ConstantValue extends BooleanObject {

    private final boolean value;

    public ConstantValue(boolean value) {
        super(BooleanObjectType.CONSTANT);
        this.value = value;
    }

    @Override
    public String toString() {
        return value ? "1" : "0";
    }

    public boolean getValue() {
        return value;
    }
}
