
import java.util.Scanner;

public class AoC_08 {

    void magic() {
        int diffStored = 0, diffEncoded = 0;

        while (sc.hasNext()) {
            char[] input = sc.next().toCharArray();
            diffStored += 2;
            diffEncoded += 2;
            boolean escaped = false;

            for (int i = 0; i < input.length; i++) {
                diffStored += !escaped && input[i] == '\\' ? 1 : 0;
                diffStored += escaped && input[i] == 'x' ? 2 : 0;
                escaped = input[i] == '\\' ? !escaped : false;
                diffEncoded += input[i] == '"' || input[i] == '\\' ? 1 : 0;
            }
        }

        System.out.println("Part One: " + diffStored);
        System.out.println("Part Two: " + diffEncoded);
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_08().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}
