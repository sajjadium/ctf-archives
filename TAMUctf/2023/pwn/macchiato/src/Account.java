public abstract class Account {
    abstract Long get(Long index);
    abstract void set(Long index, Long value);
    Long sum() {
        Long s = 0L;
        for (Long i = 0L; i < 10L; ++i) {
            s += get(i);
        }
        return s;
    }
    void withdraw(Long index, Long value) {
        set(index, get(index) - value);
    }
}
