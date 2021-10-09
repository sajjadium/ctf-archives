package jython.rts;

import java.util.*;
import java.util.function.*;

public final class Traits {
    public static record Tup2<A, B> (A fst, B snd) {}

    public enum PartialOrdering {
        POEqual, POLess, POGreater, PONone, POIllegal;

        public static <T> boolean isOrdering(BiFunction<T, T, PartialOrdering> cmpFn,
                T a, T b, PartialOrdering... want) {
            var res = cmpFn.apply(a, b);
            for (var po : want)
                if (po == res) return true;
            return false;
        }

        public static <T> boolean isGE(BiFunction<T, T, PartialOrdering> cmpFn,
                T a, T b) {
            return isOrdering(cmpFn, a, b, POEqual, POGreater);
        }
    }

    public record Trait<A>(Class<?>[] constraints, Class<A> traitOf,
                                                 Function<Interpreter, A> traitImpl) { }

    private final static HashMap<Class<?>, List<Trait<?>>> traits = new HashMap<>();

    // We define A > B iif every class constraint in A is
    // a super class to the corresponding class constraint in B, i.e. A >s B
    // With this definition, the function a.isAssignableFrom b is equivalent to:
    //     a >s b OR a == b
    private static PartialOrdering compareConstraints(Class<?>[] a, Class<?>[] b) {
        if (a.length != b.length) return PartialOrdering.POIllegal;

        var allSubset = true;
        var allSuperset = true;
        var allEquals = true;
        var noOverlapping = false;
        for (var i = 0; i < a.length; i++) {
            if (a[i] != b[i]) {
                allEquals = false;
                var isSuper = a[i].isAssignableFrom(b[i]);
                var isSub = b[i].isAssignableFrom(a[i]);
                if (isSuper) {
                    allSubset = false;
                } else if (isSub) {
                    allSuperset = false;
                } else {
                    allSubset = false;
                    allSuperset = false;
                    noOverlapping = true;
                }
            }
        }
        if (allEquals) return PartialOrdering.POEqual;
        else if (allSuperset) return PartialOrdering.POGreater;
        else if (allSubset) return PartialOrdering.POLess;
        else if (noOverlapping) return PartialOrdering.PONone;
        else return PartialOrdering.POIllegal;
    }

    public static <A> void addTrait(Class<A> itrait, Function<Interpreter, A> trait, Class<?>... constraints) {
        // Confirm that constraints are classes
        for (var cst : constraints) {
            if (cst != Object.class && cst.getSuperclass() == null)
                throw new IllegalArgumentException("subclasses constraints must be " +
                        "classes, not interfaces");
        }

        // Check the constraint length is the same
        var traitInfos = traits.computeIfAbsent(itrait, k -> new ArrayList<>());
        if (!traitInfos.isEmpty()) {
            var cstLength = traitInfos.get(0).constraints.length;
            if (cstLength != constraints.length) {
                throw new IllegalArgumentException("Invalid number of traits");
            }
        }

        // Check for any illegal overlapping of constraints
        for (var traitInfo : traitInfos) {
            PartialOrdering po = compareConstraints(traitInfo.constraints, constraints);
            if (po == PartialOrdering.POEqual || po == PartialOrdering.POIllegal)
                throw new IllegalArgumentException("Illegal overlapping of traits");
        }

        // Add trait
        traitInfos.add(new Trait<>(constraints, itrait, trait));
    }

    public static <A> A getTraitImplNonNull(Interpreter env, String msg, Class<A> trait, Class<?>... tvars) {
        var traitImpl = getTraitImpl(env, trait, tvars);
        if (traitImpl == null) throw new Errors.TypeError(env, msg);
        return traitImpl;
    }

    public static <A> A getTraitImpl(Interpreter env, Class<A> trait, Class<?>... tvars) {
        var traitInfos = traits.getOrDefault(trait, Collections.emptyList());

        // Find the trait with the minimum (most specific) constraint that fits the
        // tvars we are given.
        Trait<?> best = null;
        for (var traitInfo : traitInfos) {
            if (PartialOrdering.isGE(Traits::compareConstraints,
                    traitInfo.constraints, tvars)) {
                if (best == null || PartialOrdering.isGE(Traits::compareConstraints,
                        best.constraints, traitInfo.constraints)) {
                    best = traitInfo;
                }
            }
        }

        return best == null ? null : (A)best.traitImpl.apply(env);
    }

    private Traits() {}
}
