/// zoomies
import sun.misc.Unsafe;

public class BlazinglyFastAccount extends Account {
    static Unsafe u = (Unsafe)Challenge.load(Unsafe.class, "theUnsafe");
    long[] arr; 
    private boolean checkBounds(Long index) {
        var geMin = index.compareTo(0L) >= 0;
        var ltMax = index.compareTo(10L) < 0;
        return geMin && ltMax;
    }
    public BlazinglyFastAccount(long[] arr) {
        this.arr = arr;
    }
    public Long get(Long index) {
        var base = u.arrayBaseOffset(long[].class);
        return checkBounds(index) ? u.getLong(this.arr, base + index * 8) : 0;
    }
    public void set(Long index, Long value) {
        if (checkBounds(index)) {
            var base = u.arrayBaseOffset(long[].class);
            u.putLong(this.arr, base + index * 8, value);
        }
    }
}

