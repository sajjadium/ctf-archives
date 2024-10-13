package jython.rts;

import java.lang.reflect.Field;
import java.util.*;
import java.util.function.Function;

import static jython.rts.Errors.*;
import static jython.rts.ObjectTraits.*;
import static jython.rts.Traits.*;

public final class ObjectTraits {
    public static class NoneType {
        private NoneType() {}
    }

    public static record _Printer(String data) { }

    public interface Environmented {
        Interpreter getEnv();
    }

    public interface IsObject<A> extends Environmented {
        // IsObject<A> => A -> Class<A>
        Class<A> __class__(A self);
        // IsObject<A> => Class<A> -> String
        String __class_name__(Class<A> cls);
        // (IsReference<R>, IsObject<A>) => A -> String -> R B
        Object __attribute__(A self, String attr);
        // IsObject<A> => A -> String
        String __str__(A self);
        // IsObject<A> => A -> String
        String __repr__(A self);

        default Traits.Tup2<Object, IsReference<Object>> __attribute_ref__(A self, String attrName) {
            var attrVal = __attribute__(self, attrName);
            var trait = getTraitImplNonNull(getEnv(), "Illegal item definition",
                    IsReference.class, attrVal.getClass());
            return new Traits.Tup2<>(attrVal, trait);
        }
    }

    public interface HasAttrs<A> extends Environmented {
        // (HasAttr<A>, IsReference<R>) => A -> String -> R B -> ()
        Object __attr__(A self, String attr);

        default Traits.Tup2<Object, IsReference<Object>> __attr_ref__(A self, String attrName) {
            var attrVal = __attr__(self, attrName);
            var trait = getTraitImplNonNull(getEnv(), "Illegal item definition",
                    IsReference.class, attrVal.getClass());
            return new Traits.Tup2<>(attrVal, trait);
        }
    }

    // IsObject<A> => HasItems<A, I>
    public interface HasItems<A, I> extends Environmented {
        // (HasItems<A, I>, IsReference<R>) => A -> I -> R B
        Object __item__(A self, I item);
        default Traits.Tup2<Object, IsReference<Object>> __item_ref__(A self, I item) {
            var itemVal = __item__(self, item);
            var trait = getTraitImplNonNull(getEnv(), "Illegal item definition",
                    IsReference.class, itemVal.getClass());
            return new Traits.Tup2<>(itemVal, trait);
        }

        // (HasItems<A, I>) => A -> I -> B
        default Object __getitem__(A self, I item) {
            var itemRef = __item_ref__(self, item);
            return itemRef.snd().__get_deref__(itemRef.fst());
        }
        // HasItems<A, I> => A -> I -> B -> ()
        default void __setitem__(A self, I item, Object o) {
            var itemRef = __item_ref__(self, item);
            itemRef.snd().__set_deref__(itemRef.fst(), o);
        }
        // HasItems<A, I> => A -> I -> ()
        default void __delitem__(A self, I item) {
            var itemRef = __item_ref__(self, item);
            itemRef.snd().__del_ref__(itemRef.fst());
        }
    }

    // IsObject<R> => IsReference<R>
    public interface IsReference<R> extends Environmented {
        // IsReference<R> => R B -> B -> ()
        void __set_deref__(R self, Object o);
        // IsReference<R> => R B -> B
        Object __get_deref__(R self);
        // IsReference<R> => R B -> ()
        void __del_ref__(R self);
    }

    static {
        ObjectTraitImpl.registerTraits();
    }

    private ObjectTraits() {}
}

class ObjectTraitImpl {

    private static abstract class MemberRef<A, F> implements Environmented {
        public final A self;
        public final F member;
        public final Interpreter env;

        public MemberRef(Interpreter env, A self, F member) {
            this.env = env;
            this.self = self;
            this.member = member;
        }

        @Override
        public Interpreter getEnv() { return env; }

        public abstract Object get();

        public abstract void set(Object val);

        public abstract void delete();
    }
    // trait IsReference<Ref>
    private record IsReferenceMemberRef<A, F>(Interpreter env) implements IsReference<MemberRef<A, F>> {

        @Override
        public Interpreter getEnv() {
            return env;
        }

        @Override
        public void __set_deref__(MemberRef<A, F> self, Object o) {
            self.set(o);
        }

        @Override
        public Object __get_deref__(MemberRef<A, F> self) {
            return self.get();
        }

        @Override
        public void __del_ref__(MemberRef<A, F> self) {
            self.delete();
        }
    }

    static class ReadonlyRef<A> extends MemberRef<A, Object> {

        public ReadonlyRef(Interpreter env, A self, Object member) {
            super(env, self, member);
        }

        @Override
        public Object get() {
            return member;
        }

        @Override
        public void set(Object val) {
            throw new AttributeError(getEnv(), "Member is read-only property");
        }

        @Override
        public void delete() {
            throw new AttributeError(getEnv(), "Member is read-only property");
        }
    }

    private static class FieldRef<A> extends MemberRef<A, Field> {

        public FieldRef(Interpreter env, A self, Field member) {
            super(env, self, member);
        }

        @Override
        public void set(Object val) {
            try {
                member.setAccessible(true);
                member.set(self, val);
            } catch (IllegalArgumentException e) {
                throw new TypeError(getEnv(), member.getType());
            } catch (IllegalAccessException e) {
                throw new AttributeError(getEnv(), "Member is read-only or unaccessible");
            }
        }

        @Override
        public Object get() {
            try {
                member.setAccessible(true);
                return member.get(self);
            } catch (IllegalAccessException e) {
                throw new JavaError(e);
            }
        }

        @Override
        public void delete() {
            throw new AttributeError(getEnv(), "Member cannot be deleted");
        }
    }

    private static Field findField(Interpreter env, Class<?> cls, String name) {
        try {
            return cls.getDeclaredField(name);
        } catch (NoSuchFieldException e) {
            try {
                return cls.getField(name);
            } catch (NoSuchFieldException e2) {
                throw new AttributeError(env, cls, name);
            }
        }
    }

    // trait IsObject<Object>
    static class IsObjectObj<A> implements IsObject<A> {
        private final Interpreter env;

        IsObjectObj(Interpreter env) { this.env = env; }

        @Override
        public Interpreter getEnv() { return env; }

        @Override
        public Class<A> __class__(A self) { return (Class<A>)self.getClass(); }

        @Override
        public String __class_name__(Class<A> cls) { return cls.getName(); }

        @Override
        public Object __attribute__(A self, String attr) {
            if (attr.equals("__class__")) {
                return new ReadonlyRef<>(env, self, self.getClass());
            } else {
                var traitAttr = getTraitImpl(env, HasAttrs.class, self.getClass());
                if (traitAttr == null) {
                    return new FieldRef<>(env, self, findField(getEnv(), self.getClass(), attr));
                } else {
                    return traitAttr.__attr__(self, attr);
                }
            }
        }

        @Override
        public String __str__(A self) {
            return Objects.toString(self);
        }

        @Override
        public String __repr__(A self) {
            return __str__(self);
        }
    }

    // trait IsObject<String>
    static class IsObjectString extends IsObjectObj<String> {

        IsObjectString(Interpreter env) {
            super(env);
        }

        @Override
        public String __class_name__(Class<String> cls) {
            return "str";
        }

        @Override
        public String __str__(String self) {
            return self;
        }

        @Override
        public String __repr__(String self) {
            var sb = new StringBuilder();
            var enclosing = (self.contains("'") && !self.contains("\"")) ? '"' : '\'';
            sb.append(enclosing);
            for (char c : self.toCharArray()) {
                sb.append(switch(c) {
                    case '\n' -> "\\n";
                    case '\t' -> "\\t";
                    case '\r' -> "\\r";
                    case '\0' -> "\\0";
                    case '\\' -> "\\\\";
                    case '"', '\'' -> enclosing == c ? "\\" + c : String.valueOf(c);
                    case 0xb  -> "\\v";
                    default -> {
                        if (c >= 0x20 && c <= 0x7e) {
                            yield String.valueOf(c);
                        } else if (c <= 0xff) {
                            yield String.format("\\x%02x", (int)c);
                        } else {
                            yield String.format("\\u%04x", (int)c);
                        }
                    }
                });
            }
            sb.append(enclosing);
            return sb.toString();
        }
    }
    // trait HasItems<String>
    private record HasItemsString(Interpreter env) implements HasItems<String, Integer> {

        @Override
        public Interpreter getEnv() {
            return env;
        }

        @Override
        public Object __item__(String self, Integer item) {
            if (item < 0 || item >= self.length())
                throw new ItemError(env, self.getClass(), item);
            return new ReadonlyRef<>(env, self, String.valueOf(self.charAt(item)));
        }
    }

    // trait IsObject<Class>
    private static class IsObjectClass extends IsObjectObj<Class<?>> {
        IsObjectClass(Interpreter env) { super(env); }

        @Override
        public String __class_name__(Class<Class<?>> cls) { return "type"; }

        @Override
        public String __str__(Class<?> self) {
            var trait = getTraitImpl(getEnv(), IsObject.class, self);
            return trait == null ? "null" : String.format("'%s'", trait.__class_name__(self));
        }

        @Override
        public String __repr__(Class<?> self) {
            var trait = getTraitImpl(getEnv(), IsObject.class, self);
            return trait == null ? "null" : String.format("<class '%s'>", trait.__class_name__(self));
        }
    }
    // trait HasAttrs<Class>
    private record HasAttrClass(Interpreter env) implements HasAttrs<Class<?>> {
        @Override
        public Interpreter getEnv() {
            return env;
        }

        @Override
        public Object __attr__(Class<?> self, String attr) {
            return new ReadonlyRef<>(env, self, findField(getEnv(), self, attr));
        }
    }

    private static class ArrayRef<A> extends MemberRef<A, Integer> {
        public ArrayRef(Interpreter env, A self, Integer member) { super(env, self, member); }

        @Override
        public Object get() {
            try {
                if (self instanceof Object[]) {
                    return ((Object[]) self)[member];
                } else if (self instanceof boolean[]) {
                    return ((boolean[]) self)[member];
                } else if (self instanceof byte[]) {
                    return ((byte[]) self)[member];
                } else if (self instanceof char[]) {
                    return ((char[]) self)[member];
                } else if (self instanceof short[]) {
                    return ((short[]) self)[member];
                } else if (self instanceof int[]) {
                    return ((int[]) self)[member];
                } else if (self instanceof long[]) {
                    return ((long[]) self)[member];
                } else if (self instanceof float[]) {
                    return ((float[]) self)[member];
                } else if (self instanceof double[]) {
                    return ((double[]) self)[member];
                } else {
                    throw new InternalError("Bad object for trait");
                }
            } catch (ArrayIndexOutOfBoundsException e) {
                throw new ItemError(getEnv(), self.getClass(), member);
            } catch (ClassCastException e) {
                throw new TypeError(getEnv(), self.getClass().getComponentType());
            }
        }

        @Override
        public void set(Object val) {
            try {
                if (self instanceof Object[]) {
                    ((Object[]) self)[member] = val;
                } else if (self instanceof boolean[]) {
                    ((boolean[]) self)[member] = (Boolean)val;
                } else if (self instanceof byte[]) {
                    ((byte[]) self)[member] = (Byte)val;
                } else if (self instanceof char[]) {
                    ((char[]) self)[member] = (Character)val;
                } else if (self instanceof short[]) {
                    ((short[]) self)[member] = (Short)val;
                } else if (self instanceof int[]) {
                    ((int[]) self)[member] = (Integer)val;
                } else if (self instanceof long[]) {
                    ((long[]) self)[member] = (Long)val;
                } else if (self instanceof float[]) {
                    ((float[]) self)[member] = (Float)val;
                } else if (self instanceof double[]) {
                    ((double[]) self)[member] = (Double)val;
                } else {
                    throw new InternalError("Bad object for trait");
                }
            } catch (ArrayIndexOutOfBoundsException e) {
                throw new ItemError(getEnv(), self.getClass(), member);
            } catch (ClassCastException e) {
                throw new TypeError(getEnv(), self.getClass().getComponentType());
            }
        }

        @Override
        public void delete() {
            throw new TypeError(getEnv(), "Cannot delete from fixed array");
        }
    }

    // trait IsArray<A> => IsObject<A>
    private static class IsObjectArray extends IsObjectObj<Object> {

        IsObjectArray(Interpreter env) {
            super(env);
        }

        @Override
        public String __class_name__(Class<Object> cls) {
            return "array.array";
        }

        @Override
        public String __str__(Object self) {
            String strRep;
            String typ;
            if (self instanceof Object[] selfObj) {
                strRep = listRep(getEnv(), Arrays.asList(selfObj));
                typ = getEnv().builtins.str(self.getClass().getComponentType());
            } else if (self instanceof boolean[]) {
                strRep = Arrays.toString((boolean[]) self);
                typ = "'z'";
            } else if (self instanceof byte[]) {
                strRep = Arrays.toString((byte[]) self);
                typ = "'b'";
            } else if (self instanceof char[]) {
                strRep = Arrays.toString((char[]) self);
                typ = "'c'";
            } else if (self instanceof short[]) {
                strRep = Arrays.toString((short[]) self);
                typ = "'s'";
            } else if (self instanceof int[]) {
                strRep = Arrays.toString((int[]) self);
                typ = "'i'";
            } else if (self instanceof long[]) {
                strRep = Arrays.toString((long[]) self);
                typ = "'j'";
            } else if (self instanceof float[]) {
                strRep = Arrays.toString((float[]) self);
                typ = "'f'";
            } else if (self instanceof double[]) {
                strRep = Arrays.toString((double[]) self);
                typ = "'d'";
            } else {
                throw new InternalError("Bad object for trait");
            }
            return String.format("array(%s, %s)", typ, strRep);
        }
    }
    // trait IsArray<A> => HasItems<A, Integer>
    private record HasItemsArray(Interpreter env) implements HasItems<Object, Integer> {

        @Override
        public Interpreter getEnv() {
            return env;
        }

        @Override
        public Object __item__(Object self, Integer item) {
            return new ArrayRef<>(env, self, item);
        }
    }

    private static class ListRef<A extends List<Object>> extends MemberRef<A, Integer> {
        public ListRef(Interpreter env, A self, Integer member) { super(env, self, member); }

        @Override
        public Object get() {
            try {
                return self.get(member);
            } catch (IndexOutOfBoundsException e) {
                throw new ItemError(getEnv(), self.getClass(), member);
            }
        }

        @Override
        public void set(Object val) {
            try {
                self.set(member, val);
            } catch (IndexOutOfBoundsException e) {
                throw new ItemError(getEnv(), self.getClass(), member);
            }
        }

        @Override
        public void delete() {
            try {
                self.remove(member);
            } catch (IndexOutOfBoundsException e) {
                throw new ItemError(getEnv(), self.getClass(), member);
            }
        }
    }
    // trait Collection<A> => IsObject<A>
    private static class IsObjectCollection<A extends Collection<?>> extends IsObjectObj<A> {
        IsObjectCollection(Interpreter env) {
            super(env);
        }

        @Override
        public String __class_name__(Class<A> cls) {
            return "list";
        }

        @Override
        public String __str__(A self) {
            return listRep(getEnv(), self);
        }
    }
    // trait List<A> => HasItems<A, Integer>
    private record HasItemsList<A extends List<Object>>(Interpreter env) implements HasItems<A, Integer> {

        @Override
        public Interpreter getEnv() {
            return env;
        }

        @Override
        public Object __item__(A self, Integer item) {
            return new ListRef<>(getEnv(), self, item);
        }
    }

    private static class MapRef<A extends Map<K, Object>, K> extends MemberRef<A, K> {

        public MapRef(Interpreter env, A self, K member) {
            super(env, self, member);
        }

        @Override
        public void set(Object val) {
            self.put(member, val);
        }

        @Override
        public Object get() {
            return self.get(member);
        }

        public void delete() {
            self.remove(member);
        }
    }
    // trait Map<A, K> => IsObject<A>
    private static class IsObjectMap<A extends Map<K, Object>, K> extends IsObjectObj<A> {
        IsObjectMap(Interpreter env) {
            super(env);
        }

        @Override
        public String __class_name__(Class<A> cls) {
            return "dict";
        }

        @Override
        public String __str__(A self) {
            var sb = new StringBuilder();
            var first = true;
            sb.append('{');
            for (var ent : self.entrySet()) {
                if (first) first = false;
                else sb.append(", ");
                sb.append(getEnv().builtins.str(ent.getKey()));
                sb.append(": ");
                sb.append(getEnv().builtins.str(ent.getValue()));
            }
            sb.append('}');
            return sb.toString();
        }
    }
    // trait Map<A, K> => HasItems<A, K>
    private record HasItemsMap<A extends Map<K, Object>, K>(Interpreter env) implements HasItems<A, K> {

        @Override
        public Interpreter getEnv() {
            return env;
        }

        @Override
        public Object __item__(A self, K item) {
            return new MapRef<>(getEnv(), self, item);
        }
    }

    // trait IsObject<Integer>
    public static class IsObjectInteger extends IsObjectObj<Integer> {
        IsObjectInteger(Interpreter env) {
            super(env);
        }

        @Override
        public String __class_name__(Class<Integer> cls) {
            return "int";
        }
    }
    // trait IsObject<Long>
    public static class IsObjectLong extends IsObjectObj<Long> {
        IsObjectLong(Interpreter env) {
            super(env);
        }

        @Override
        public String __class_name__(Class<Long> cls) {
            return "long";
        }

        @Override
        public String __str__(Long self) {
            return self.toString() + "L";
        }
    }
    // trait IsObject<None>
    public static class IsObjectNone extends IsObjectObj<NoneType> {
        IsObjectNone(Interpreter env) {
            super(env);
        }

        @Override
        public String __class_name__(Class<NoneType> cls) {
            return "NoneType";
        }

        @Override
        public String __str__(NoneType self) {
            return "";
        }
    }
    // trait IsObject<_Printer>
    public static class IsObjectPrinter extends IsObjectObj<_Printer> {
        IsObjectPrinter(Interpreter env) {
            super(env);
        }

        @Override
        public String __class_name__(Class<_Printer> cls) {
            return "_Printer";
        }

        @Override
        public String __str__(_Printer self) {
            return self.data();
        }
    }


    private static String listRep(Interpreter env, Iterable<?> selfObj) {
        String strRep;
        boolean first = true;
        StringBuilder strRepBuilder = new StringBuilder("[");
        for (Object elem : selfObj) {
            if (first) first = false;
            else strRepBuilder.append(", ");
            strRepBuilder.append(env.builtins.str(elem));
        }
        strRepBuilder.append(']');
        strRep = strRepBuilder.toString();
        return strRep;
    }

    private static <T> void addArrayTrait(Class<T> traitType, Function<Interpreter, T> trait, Class<?>... after) {
        Class<?>[] arrayTypes = {
                Object[].class, boolean[].class, byte[].class, char[].class, short[].class,
                int[].class, long[].class, float[].class, double[].class
        };

        for (var arrayType : arrayTypes) {
            var tvars = new Class<?>[after.length + 1];
            System.arraycopy(after, 0, tvars, 1, after.length);
            tvars[0] = arrayType;
            addTrait(traitType, trait, tvars);
        }
    }

    static void registerTraits() {
        // Special object traits
        addTrait(IsObject.class, IsObjectObj::new, Object.class);
        addTrait(IsObject.class, IsObjectClass::new, Class.class);
        addTrait(IsObject.class, IsObjectInteger::new, Integer.class);
        addTrait(IsObject.class, IsObjectLong::new, Long.class);
        addTrait(IsObject.class, IsObjectNone::new, NoneType.class);
        addTrait(IsObject.class, IsObjectPrinter::new, _Printer.class);

        addTrait(IsObject.class, IsObjectString::new, String.class);
        addTrait(HasItems.class, HasItemsString::new, String.class, Integer.class);

        addTrait(HasAttrs.class, HasAttrClass::new, Class.class);
        addTrait(IsReference.class, IsReferenceMemberRef::new, MemberRef.class);

        // Array Traits
        addArrayTrait(HasItems.class, HasItemsArray::new, Integer.class);
        addArrayTrait(IsObject.class, IsObjectArray::new);

        // List traits
        addTrait(IsObject.class, IsObjectCollection::new, AbstractCollection.class);
        addTrait(HasItems.class, HasItemsList::new, AbstractList.class, Integer.class);

        // Dict traits
        addTrait(IsObject.class, IsObjectMap::new, AbstractMap.class);
        addTrait(HasItems.class, HasItemsMap::new, AbstractMap.class, Object.class);
    }

    private ObjectTraitImpl() {}
}