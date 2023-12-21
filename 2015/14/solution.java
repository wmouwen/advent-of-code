
import java.util.ArrayList;
import java.util.Scanner;

public class AoC_14 {

    class Reindeer {

        int speed, sprint, cycle, distance = 0, points = 0;

        Reindeer(String[] input) {
            speed = Integer.valueOf(input[3]);
            sprint = Integer.valueOf(input[6]);
            cycle = sprint + Integer.valueOf(input[13]);
        }
    }

    void magic() {
        ArrayList<Reindeer> reindeers = new ArrayList<>();
        while (sc.hasNextLine()) {
            reindeers.add(new Reindeer(sc.nextLine().split(" ")));
        }

        int maxDistance = 0, maxPoints = 0;
        for (int tick = 0; tick < 2503; tick++) {
            for (Reindeer reindeer : reindeers) {
                maxDistance = Math.max(maxDistance, reindeer.distance += tick % reindeer.cycle < reindeer.sprint ? reindeer.speed : 0);
            }
            for (Reindeer reindeer : reindeers) {
                maxPoints = Math.max(maxPoints, reindeer.points += reindeer.distance == maxDistance ? 1 : 0);
            }
        }
        System.out.println("Part One: " + maxDistance);
        System.out.println("Part Two: " + maxPoints);
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_14().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}
