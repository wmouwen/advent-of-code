
import java.util.ArrayList;
import java.util.Scanner;

public class AoC_17 {
    
    class Triple {
        int min = Integer.MAX_VALUE, minCount = 0, totalCount = 0;
    }

    void magic() {
        ArrayList<Integer> containers = new ArrayList<>();
        while (sc.hasNextInt()) {
            containers.add(sc.nextInt());
        }
        
        Triple answer = new Triple();
        recurse(containers, 150, 0, 0, answer);
        
        System.out.println("Part One: " + answer.totalCount);
        System.out.println("Part Two: " + answer.minCount);
    }
    
    void recurse(ArrayList<Integer> containers, int left, int depth, int used, Triple answer) {
        if (depth == containers.size()) {
            if (left == 0) {
                answer.totalCount++;
                if (used == answer.min) {
                    answer.minCount++;
                } else if (used < answer.min) {
                    answer.min = used;
                    answer.minCount = 1;
                }
            }
            return;
        }
        
        recurse(containers, left, depth + 1, used, answer);
        if (containers.get(depth) <= left) {
            recurse(containers, left - containers.get(depth), depth + 1, used + 1, answer);
        }
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_17().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}
