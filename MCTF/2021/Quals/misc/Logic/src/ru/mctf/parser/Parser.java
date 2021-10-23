package ru.mctf.parser;

import java.util.*;

public class Parser {

    private final Map<String, Variable> variables = new HashMap<>();
    private final List<BooleanObject> allObjects = new ArrayList<>();

    public BooleanObject parse(String equation) {
        if(equation.indexOf(' ') == -1) {
            return parseConstantOrVariable(equation);
        }

        if(equation.startsWith("(") && equation.endsWith(")")) {
            equation = equation.substring(1, equation.length() - 1);
        }

        List<String> parts = splitToParts(equation);

        return parseOperator(parts);
    }

    private List<String> splitToParts(String equation) {
        List<String> parts = new ArrayList<>();

        outer:
        while (true) {
            int opens = 0;
            for (int i = 0; i < equation.length(); i++) {
                if (equation.charAt(i) == '(') {
                    opens++;
                } else if (equation.charAt(i) == ')') {
                    if(opens == 0) {
                        throw new IllegalStateException();
                    }

                    opens--;
                } else if (equation.charAt(i) == ' ' && opens == 0) {
                    parts.add(equation.substring(0, i));
                    equation = equation.substring(i + 1);
                    continue outer;
                }
            }

            if(opens != 0) {
                throw new IllegalStateException();
            }

            parts.add(equation);
            break;
        }
        return parts;
    }

    private BooleanObject parseConstantOrVariable(String equation) {
        if(equation.equals("0")) {
            final ConstantValue constant = new ConstantValue(false);
            allObjects.add(constant);
            return constant;
        } else if(equation.equals("1")) {
            final ConstantValue constant = new ConstantValue(true);
            allObjects.add(constant);
            return constant;
        } else {
            final Variable variable = variables.computeIfAbsent(equation, Variable::new);
            allObjects.add(variable);
            return variable;
        }
    }

    private Operator parseOperator(List<String> parts) {
        if(parts.size() == 2 && parts.get(0).equals("not")) {
            final BooleanObject second = parse(parts.get(1));

            final Operator operator = new Operator(OperatorType.NOT, List.of(second));
            second.setParent(operator);

            allObjects.add(operator);
            return operator;
        } else if(parts.size() == 3){
            final OperatorType type = OperatorType.valueOf(parts.get(1).toUpperCase());
            final BooleanObject first = parse(parts.get(0));
            final BooleanObject second = parse(parts.get(2));

            final Operator operator = new Operator(type, List.of(first, second));

            first.setParent(operator);
            second.setParent(operator);

            allObjects.add(operator);
            return operator;
        } else {
            throw new IllegalStateException();
        }
    }

    public List<BooleanObject> getAllObjects() {
        return allObjects;
    }
}
