
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class AoC_05 {

    void magic() {
        ArrayList<Character> vowels = new ArrayList<>(Arrays.asList('a', 'e', 'i', 'o', 'u'));
        ArrayList<String> forbiddenCombos = new ArrayList<>(Arrays.asList("ab", "cd", "pq", "xy"));
        int oldRulesNice = 0, newRulesNice = 0;

        while (sc.hasNextLine()) {
            String inputLine = sc.nextLine();
            char[] input = inputLine.toCharArray();
            int vowelCount = 0;
            boolean twiceInARow = false,
                    comboFound = false,
                    repetitiveChar = false,
                    doubleDouble = false;
            ArrayList<String> haystack = new ArrayList<>();

            for (int i = 0; i < input.length; i++) {
                vowelCount += vowels.contains(input[i]) ? 1 : 0;
                if (i > 0) {
                    twiceInARow |= input[i] == input[i - 1];
                    comboFound |= forbiddenCombos.contains(input[i - 1] + "" + input[i]);
                    if (i + 1 < input.length) {
                        doubleDouble |= haystack.contains(inputLine.substring(i, i + 2));
                        haystack.add(inputLine.substring(i - 1, i + 1));
                    }
                }
                if (i > 1) {
                    repetitiveChar |= input[i] == input[i - 2];
                }
            }
            oldRulesNice += vowelCount >= 3 && twiceInARow && !comboFound ? 1 : 0;
            newRulesNice += repetitiveChar && doubleDouble ? 1 : 0;
        }

        System.out.println("Part One: " + oldRulesNice);
        System.out.println("Part Two: " + newRulesNice);
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) throws Exception {
        long startTime = System.currentTimeMillis();
        new AoC_05().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}
