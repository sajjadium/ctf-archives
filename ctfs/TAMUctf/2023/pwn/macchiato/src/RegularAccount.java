public class RegularAccount extends Account {
    Long[] arr; 
    public RegularAccount(Long[] arr) {
        this.arr = arr;
    }
    public Long get(Long index) {
        return this.arr[index.intValue()];
    }
    public void set(Long index, Long value) {
        this.arr[index.intValue()] = value;
    }
}
