import java.time.Instant;
public class CustomRandom {
    private long seed;
    private final long i = 3473400794307473L;

    public CustomRandom() {
        this.seed = Instant.now().getEpochSecond() ^ i;
    }

    public void setSeed(long seed) {
        this.seed = seed ^ i;
    }

    public long nextLong() {
        long m = 1L << 52;
        long c = 4164880461924199L;
        long a = 2760624790958533L;
        seed = (a *seed+ c) & (m -1L);
        return seed;
    }
}
