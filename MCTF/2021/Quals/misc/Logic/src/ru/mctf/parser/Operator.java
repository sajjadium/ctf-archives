package ru.mctf.parser;

import java.util.List;

public class Operator extends BooleanObject {

    private final OperatorType operatorType;
    private List<BooleanObject> inputs;

    public Operator(OperatorType operatorType, List<BooleanObject> inputs) {
        super(BooleanObjectType.OPERATOR);
        this.operatorType = operatorType;
        this.inputs = inputs;
    }

    @Override
    public String toString() {
        if(operatorType == OperatorType.NOT) {
            return String.format("(not %s)", inputs.get(0).toString());
        } else {
            return String.format("(%s %s %s)",
                    inputs.get(0).toString(),
                    operatorType.name().toLowerCase(),
                    inputs.get(1).toString());
        }
    }

    public OperatorType getOperatorType() {
        return operatorType;
    }

    public List<BooleanObject> getInputs() {
        return inputs;
    }

    public void setInputs(List<BooleanObject> inputs) {
        this.inputs = inputs;
    }
}
