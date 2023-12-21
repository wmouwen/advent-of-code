
import java.util.Scanner;

public class AoC_20 {

    void magic() {
        int input = sc.nextInt(), partOne = Integer.MAX_VALUE, partTwo = Integer.MAX_VALUE;
        long[] housesOne = new long[1000000], housesTwo = new long[housesOne.length];
        
        for (int i = 1; i < housesOne.length; i++) {
            for (int j = 1; i * j < housesOne.length; j++) {
                housesOne[i * j] += 10 * i;
                housesTwo[i * j] += j <= 50 ? 11 * i : 0;
            }
            if (housesOne[i] >= input) {
                partOne = Math.min(i, partOne);
            }
            if (housesTwo[i] >= input) {
                partTwo = Math.min(i, partTwo);
            }
        }
        
        System.out.println("Part One: " + partOne);
        System.out.println("Part Two: " + partTwo);
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_20().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}
