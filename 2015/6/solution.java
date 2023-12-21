
import java.util.Scanner;

public class AoC_06 {

    enum Action {

        ON, OFF, TOGGLE
    };

    final static int GRIDSIZE = 1000;

    void magic() {
        boolean[][] lit = new boolean[GRIDSIZE][GRIDSIZE];
        int[][] brightness = new int[GRIDSIZE][GRIDSIZE];

        while (sc.hasNextLine()) {
            String[] input = sc.nextLine().toUpperCase().replace("TURN ", "").split(" ");
            Action action = Action.valueOf(input[0]);
            int minX = Integer.parseInt(input[1].split(",")[0]),
                    minY = Integer.parseInt(input[1].split(",")[1]),
                    maxX = Integer.parseInt(input[3].split(",")[0]),
                    maxY = Integer.parseInt(input[3].split(",")[1]);

            for (int x = minX; x <= maxX; x++) {
                for (int y = minY; y <= maxY; y++) {
                    switch (action) {
                        case ON:
                            lit[x][y] = true;
                            brightness[x][y]++;
                            break;
                        case OFF:
                            lit[x][y] = false;
                            brightness[x][y] = Math.max(0, --brightness[x][y]);
                            break;
                        case TOGGLE:
                            lit[x][y] = !lit[x][y];
                            brightness[x][y] += 2;
                            break;
                    }
                }
            }
        }

        long litCount = 0, totalBrightness = 0;
        for (int x = 0; x < GRIDSIZE; x++) {
            for (int y = 0; y < GRIDSIZE; y++) {
                litCount += lit[x][y] ? 1 : 0;
                totalBrightness += brightness[x][y];
            }
        }

        System.out.println("Part One: " + litCount);
        System.out.println("Part Two: " + totalBrightness);
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_06().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}

