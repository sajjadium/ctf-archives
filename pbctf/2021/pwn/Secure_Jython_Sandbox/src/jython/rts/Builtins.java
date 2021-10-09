package jython.rts;

import static java.lang.String.format;
import static jython.rts.Errors.*;
import static jython.rts.ObjectTraits.*;
import static jython.rts.Traits.*;

public record Builtins(Interpreter env) implements ObjectTraits.Environmented {


    @Override
    public Interpreter getEnv() {
        return env;
    }

    public String str(Object o) {
        if (o == null) return "None";
        else {
            var trait = getTraitImpl(env, ObjectTraits.IsObject.class, o.getClass());
            return trait == null ? "<unknown>" : trait.__str__(o);
        }
    }

    public String repr(Object o) {
        if (o == null) return "None";
        else {
            var trait = getTraitImpl(env, ObjectTraits.IsObject.class, o.getClass());
            return trait == null ? "<unknown>" : trait.__repr__(o);
        }
    }

    public Tup2<Object, IsReference<Object>> attr(Object self, Object attr) {
        if (attr instanceof String attrName) {
            if (self == null) throw new AttributeError(env, NoneType.class, attrName);
            var trait = getTraitImpl(env, ObjectTraits.IsObject.class, self.getClass());
            if (trait == null) throw new AttributeError(env, self.getClass(), attrName);
            return trait.__attribute_ref__(self, attrName);
        } else {
            throw new TypeError(env, "attribute name must be a string");
        }
    }

    public Object getattr(Object self, Object attr) {
        var ref = attr(self, attr);
        return ref.snd().__get_deref__(ref.fst());
    }

    public Tup2<Object, IsReference<Object>> item(Object self, Object item) {
        if (self == null) throw new ItemError(env, NoneType.class, item);
        return getTraitImplNonNull(env, format("%s object is not subscriptable", str(self.getClass())),
                HasItems.class, self.getClass(), item.getClass()).__item_ref__(self, item);
    }
}
