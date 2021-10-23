package ru.mctf;

import ru.mctf.parser.BooleanObject;
import ru.mctf.parser.ConstantValue;
import ru.mctf.parser.Operator;
import ru.mctf.parser.Variable;

import java.io.DataOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.List;

public class BinaryFormatWriter {

    public static void write(List<BooleanObject> objects, File outFile) throws IOException {
        try (DataOutputStream out = new DataOutputStream(new FileOutputStream(outFile))) {
            out.writeShort(objects.size());
            for (BooleanObject o : objects) {
                out.writeShort(o.getId());
                out.writeByte(o.getType().ordinal());
                out.writeShort(o.getParent() != null ? o.getParent().getId() : 0);

                switch (o.getType()) {
                    case CONSTANT:
                        out.writeBoolean(((ConstantValue) o).getValue());
                        break;
                    case VARIABLE:
                        Variable variable = (Variable) o;
                        out.writeByte(variable.getName().length());
                        out.writeBytes(variable.getName());
                        break;
                    case OPERATOR:
                        Operator operator = (Operator) o;
                        out.writeByte(operator.getOperatorType().ordinal());
                        out.writeByte(operator.getInputs().size());
                        for (BooleanObject input : operator.getInputs()) {
                            out.writeShort(input.getId());
                        }
                }
            }
        }
    }

}
