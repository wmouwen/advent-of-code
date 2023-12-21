
import java.util.Scanner;

public class AoC_10 {

    void magic() {
        StringBuilder output = new StringBuilder(sc.nextLine());
        
        for (int iteration = 1; iteration <= 50; iteration++) {
            char input[] = output.toString().toCharArray(), previous = input[0];
            output = new StringBuilder((int)(input.length * 1.4));
            int count = 1;

            for (int i = 1; i < input.length; i++, count++) {
                if (input[i] != previous) {
                    output.append(count).append(previous);
                    previous = input[i];
                    count = 0;
                }
            }
            output.append(count).append(previous);

            if (iteration == 40) {
                System.out.println("Part One: " + output.length());
            }
        }
        System.out.println("Part Two: " + output.length());
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_10().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}

