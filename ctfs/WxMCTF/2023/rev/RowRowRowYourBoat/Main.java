import java.util.*;
import java.io.*;
import java.util.stream.*;
import java.util.function.*;

public class Main {
    public static void main(String[] args) {
        System.out.print((char) IntStream.of((int) 'w').findFirst().getAsInt());
        System.out.print((char) IntStream.range(0, (int) 'x').count());
        System.out.print((char) IntStream.rangeClosed(1, ((int) 'm') * 2).summaryStatistics().getAverage());
        IntStream.concat(IntStream.concat(IntStream.of((int) 'c'), IntStream.of((int) 't')), IntStream.of((int) 'f')).forEach(e -> System.out.print((char) e));
        System.out.print((char) Arrays.stream(new String[]{"mxwctf{boo_are_you_scard}", "mxwctf{this_is_not_the_flag}", "mxwctf{stop_trying}", "mxwctf{why_are_you_reading_this}", "mxwctf{gtfo_ofhere}"}).mapToInt(e -> e.length()).sum());
        System.out.print((char) (IntStream.range(1, 100000).mapToLong(e -> LongStream.range(1, e).sum()).sum() % 7509));
        System.out.print((char) (IntStream.range(1, 10000000).mapToLong(e -> LongStream.range(1, e).sum()).sum() % 3574));
        System.out.print((char) (IntStream.range(1, 696986).filter(e -> LongStream.range(1, e + 1).reduce((a, b) -> (a * (b % 0x10000) % 0x10000)).getAsLong() == 0).count() % 127));
        System.out.print((char) IntStream.range(69420, 69515).count());
        System.out.print((char) ((IntStream.range(0, 19465212).mapToObj(e -> "jdabtieu").reduce((a, b) -> a + b).get().replaceAll("jda.tieu", "bruh").length()) / 4097936 ^ 102));
        System.out.print((char) ("free".chars().filter(e -> (e & 16) != 0).findFirst().getAsInt()));
        System.out.print((char) IntStream.range(0, 96).max().getAsInt());
        System.out.print((char) (IntStream.range(0, 42).mapToObj(e -> "wxmctf{").reduce((a, b) -> a + a).get().length() % 134 ^ 62));
        System.out.print((char) (IntStream.range(0, 4).mapToObj(e -> "four").mapToInt(e -> e.length()).sum() / 4 + 44 + 4));
        System.out.print((char) (IntStream.range(32, 192168101).mapToObj(e -> String.valueOf((char) e) + "ava").reduce((a, b) -> a + b).get().indexOf("yava") ^ 274));
        System.out.print((char) (IntStream.range(6969, 42042069 - 172).mapToObj(e -> "\u0000").reduce((a, b) -> a + b).get() + "\u0003\u0004").hashCode());
        System.out.println((char) IntStream.of((int) '}').findFirst().getAsInt());
    }
}