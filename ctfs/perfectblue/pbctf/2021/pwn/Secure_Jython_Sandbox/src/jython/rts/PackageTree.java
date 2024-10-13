package jython.rts;

import jython.rts.ObjectTraits.HasAttrs;

import java.util.HashMap;

public final class PackageTree {
    public static final PackageTree ROOT = new PackageTree(null);

    private final HashMap<String, PackageTree> childrenPkgs = new HashMap<>();
    private final HashMap<String, Class<?>> childrenClasses = new HashMap<>();
    public final String name;

    private PackageTree(String name) {
        this.name = name;
    }

    public Object findMember(Interpreter env, String simpleName) {
        if (childrenPkgs.containsKey(simpleName))
            return childrenPkgs.get(simpleName);
        if (childrenClasses.containsKey(simpleName))
            return childrenClasses.get(simpleName);

        try {
            var cls = Class.forName(name + "." + simpleName);
            childrenClasses.put(simpleName, cls);
            return cls;
        } catch (ClassNotFoundException e) {
            throw new Errors.AttributeError(env, getClass(), simpleName);
        }
    }

    public static void addPackage(String name) {
        try {
            var cls = Class.forName(name);
            var packageName = name.substring(0, name.lastIndexOf('.'));
            if (!packageName.isEmpty())
                addPackageName(packageName);
        } catch (ClassNotFoundException e) { }
    }

    public static void updatePkgs() {
        for (var pkg : Package.getPackages()) {
            addPackageName(pkg.getName());
        }
    }

    private static void addPackageName(String pkg) {
        var sb = new StringBuilder();
        var node = ROOT;
        for (var part : pkg.split("\\.")) {
            sb.append(part);
            node = node.childrenPkgs.computeIfAbsent(part, unused -> new PackageTree(sb.toString()));
            sb.append('.');
        }
    }

    static {
        updatePkgs();
        Traits.addTrait(ObjectTraits.IsObject.class, PackageTreeTraits.IsObjectPackageTree::new, PackageTree.class);
        Traits.addTrait(HasAttrs.class, PackageTreeTraits.HasAttrsPackageTree::new, PackageTree.class);
    }
}

class PackageTreeTraits {
    static class IsObjectPackageTree extends ObjectTraitImpl.IsObjectObj<PackageTree> {
        IsObjectPackageTree(Interpreter env) {
            super(env);
        }

        @Override
        public String __class_name__(Class<PackageTree> cls) {
            return "javapackage";
        }

        @Override
        public String __str__(PackageTree self) {
            return "package " + self.name;
        }
    }

    record HasAttrsPackageTree(Interpreter env) implements HasAttrs<PackageTree> {

        @Override
        public Interpreter getEnv() {
            return env;
        }

        @Override
        public Object __attr__(PackageTree self, String attr) {
            return new ObjectTraitImpl.ReadonlyRef<>(env, self, self.findMember(env, attr));
        }
    }
}
