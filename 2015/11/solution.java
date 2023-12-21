
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class AoC_11 {

    void magic() {
        String password = sc.next();
        System.out.println("Part One: " + (password = nextPassword(password)));
        System.out.println("Part Two: " + nextPassword(password));
    }

    String nextPassword(String input) {
        ArrayList<Character> forbidden = new ArrayList<>(Arrays.asList('i', 'o', 'l'));
        char[] password = input.toCharArray();
        boolean straight, forbiddenChar, inPair;
        int pairs;
        do {
            for (int i = password.length - 1; i >= 0; i--) {
                if (password[i]++ != 'z') {
                    break;
                }
                password[i] = 'a';
            }

            straight = forbiddenChar = inPair = false;
            pairs = 0;
            for (int i = 0; i < password.length; i++) {
                forbiddenChar |= forbidden.contains(password[i]);
                straight |= i >= 2 && password[i] == password[i - 1] + 1 && password[i - 1] == password[i - 2] + 1;
                inPair = !inPair && i >= 1 && password[i] == password[i - 1];
                pairs += inPair ? 1 : 0;
            }
        } while (!straight || forbiddenChar || pairs < 2);
        return String.valueOf(password);
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_11().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}
