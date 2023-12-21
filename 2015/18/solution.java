
import java.util.Scanner;

public class AoC_18 {

    void magic() {
        boolean[][] gridOne = new boolean[100][100], gridTwo = new boolean[gridOne.length][gridOne[0].length];
        for (int y = 0; y < gridOne[0].length; y++) {
            char[] input = sc.nextLine().toCharArray();
            for (int x = 0; x < gridOne.length; x++) {
                gridOne[x][y] = gridTwo[x][y] = input[x] == '#';
            }
        }

        lightCorners(gridTwo);
        for (int i = 0; i < 100; i++) {
            gridOne = GameOfLife(gridOne);
            gridTwo = GameOfLife(gridTwo);
            lightCorners(gridTwo);
        }

        System.out.println("Part One: " + countLights(gridOne));
        System.out.println("Part Two: " + countLights(gridTwo));
    }

    boolean[][] GameOfLife(boolean[][] old) {
        boolean[][] grid = new boolean[old.length][old[0].length];
        for (int y = 0; y < old[0].length; y++) {
            for (int x = 0; x < old.length; x++) {
                int neighbors = countNeighbors(old, x, y);
                grid[x][y] = neighbors == 3 || (old[x][y] && neighbors == 2);
            }
        }
        return grid;
    }

    void lightCorners(boolean[][] grid) {
        grid[0][0] = true;
        grid[grid.length - 1][0] = true;
        grid[0][grid[0].length - 1] = true;
        grid[grid.length - 1][grid[0].length - 1] = true;
    }

    int countLights(boolean[][] grid) {
        int count = 0;
        for (boolean[] row : grid) {
            for (boolean light : row) {
                count += light ? 1 : 0;
            }
        }
        return count;
    }

    int countNeighbors(boolean[][] grid, int x, int y) {
        int count = 0;
        for (int ny = Math.max(0, y - 1); ny <= Math.min(grid[0].length - 1, y + 1); ny++) {
            for (int nx = Math.max(0, x - 1); nx <= Math.min(grid.length - 1, x + 1); nx++) {
                count += grid[nx][ny] && (nx != x || ny != y) ? 1 : 0;
            }
        }
        return count;
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_18().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}

