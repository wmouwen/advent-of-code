
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class AoC_09 {

    ArrayList<String> visited;
    HashMap<String, HashMap<String, Integer>> cities;

    class MinMax {

        int min = Integer.MAX_VALUE, max = Integer.MIN_VALUE;

        void update(int input) {
            min = Math.min(min, input);
            max = Math.max(max, input);
        }
    }

    void magic() {
        for (cities = new HashMap<>(); sc.hasNextLine();) {
            String[] input = sc.nextLine().split(" ");
            if (!cities.containsKey(input[0])) {
                cities.put(input[0], new HashMap<String, Integer>());
            }
            if (!cities.containsKey(input[2])) {
                cities.put(input[2], new HashMap<String, Integer>());
            }
            cities.get(input[0]).put(input[2], Integer.parseInt(input[4]));
            cities.get(input[2]).put(input[0], Integer.parseInt(input[4]));
        }

        MinMax result = new MinMax();
        visited = new ArrayList<>();
        for (String origin : cities.keySet()) {
            DFS(origin, 0, result);
        }
        System.out.println("Part One: " + result.min);
        System.out.println("Part Two: " + result.max);
    }

    void DFS(String origin, int pathLength, MinMax result) {
        if (visited.size() + 1 == cities.size()) {
            result.update(pathLength);
            return;
        }

        visited.add(origin);
        HashMap<String, Integer> distances = cities.get(origin);
        for (String destination : distances.keySet()) {
            if (!visited.contains(destination)) {
                DFS(destination, pathLength + distances.get(destination), result);
            }
        }
        visited.remove(origin);
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_09().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}

