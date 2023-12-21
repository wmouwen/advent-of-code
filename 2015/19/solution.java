
import java.util.*;

public class AoC_19 {

    class Pair {

        String left, right;

        Pair(String left, String right) {
            this.left = left;
            this.right = right;
        }
    }

    void magic() {
        ArrayList<Pair> substitutions = new ArrayList<>();
        for (String[] input = sc.nextLine().split(" "); input.length == 3; input = sc.nextLine().split(" ")) {
            substitutions.add(new Pair(input[0], input[2]));
        }
        String molecule = sc.nextLine();

        HashSet<String> outcomes = new HashSet<>();
        for (Pair sub : substitutions) {
            for (int index = molecule.indexOf(sub.left); index >= 0; index = molecule.indexOf(sub.left, index + 1)) {
                outcomes.add(molecule.substring(0, index)
                        + sub.right
                        + molecule.substring(index + sub.left.length()));
            }
        }
        System.out.println("Part One: " + outcomes.size());

        long actions = -1;
        for (int i = 0; i < molecule.length(); i++) {
            if (molecule.charAt(i) == 'Y'
                    || (molecule.charAt(i) == 'n' && molecule.charAt(i - 1) == 'R')
                    || (molecule.charAt(i) == 'r' && molecule.charAt(i - 1) == 'A')) {
                actions--;
            } else if ('A' <= molecule.charAt(i) && molecule.charAt(i) <= 'Z') {
                actions++;
            }
        }
        System.out.println("Part Two: " + actions);
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_19().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}

