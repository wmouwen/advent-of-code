
import java.util.HashMap;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class AoC_16 {

    void magic() {
        HashMap<String, Integer> correctSue = new HashMap<>();
        correctSue.put("children", 3);
        correctSue.put("cats", 7);
        correctSue.put("samoyeds", 2);
        correctSue.put("pomeranians", 3);
        correctSue.put("akitas", 0);
        correctSue.put("vizslas", 0);
        correctSue.put("goldfish", 5);
        correctSue.put("trees", 3);
        correctSue.put("cars", 2);
        correctSue.put("perfumes", 1);

        int partOne = 0, partTwo = 0;
        while (sc.hasNextLine() && (partOne == 0 || partTwo == 0)) {
            String input = sc.nextLine();
            boolean isPartOne = true, isPartTwo = true;
            for (Matcher matcher = Pattern.compile("([a-z]+): (-?\\d+)").matcher(input); matcher.find();) {
                isPartOne &= correctSue.get(matcher.group(1)) == Integer.valueOf(matcher.group(2));
                switch (matcher.group(1)) {
                    case "cats":
                    case "trees":
                        isPartTwo &= correctSue.get(matcher.group(1)) < Integer.valueOf(matcher.group(2));
                        break;
                    case "pomeranians":
                    case "goldfish":
                        isPartTwo &= correctSue.get(matcher.group(1)) > Integer.valueOf(matcher.group(2));
                        break;
                    default:
                        isPartTwo &= correctSue.get(matcher.group(1)) == Integer.valueOf(matcher.group(2));
                        break;
                }
            }
            if (isPartOne) {
                partOne = Integer.valueOf(input.split(" ")[1].substring(0, input.split(" ")[1].length() - 1));
            }
            if (isPartTwo) {
                partTwo = Integer.valueOf(input.split(" ")[1].substring(0, input.split(" ")[1].length() - 1));
            }
        }
        System.out.println("Part One: " + partOne);
        System.out.println("Part Two: " + partTwo);
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_16().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}
