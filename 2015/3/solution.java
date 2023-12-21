import java.util.Scanner;

public class PerfectlySphericalHousesInAVacuum {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) throws Exception {
        char[] input = sc.nextLine().trim().toCharArray();
        int sX = input.length + 1,
                sY = input.length + 1,
                dX[] = new int[]{input.length / 2 + 1, input.length / 2 + 1},
                dY[] = new int[]{input.length / 2 + 1, input.length / 2 + 1},
                visitedSingleCount = 1,
                visitedDoubleCount = 1;
        boolean[][] visitedSingle = new boolean[2 * input.length + 1][2 * input.length + 1],
                visitedDouble = new boolean[input.length + 1][input.length + 1];
        visitedSingle[sX][sY] = visitedDouble[dX[0]][dY[0]] = true;

        for (int i = 0; i < input.length; i++) {
            switch (input[i]) {
                case '^':
                    sY++;
                    dY[i % 2]++;
                    break;
                case '>':
                    sX++;
                    dX[i % 2]++;
                    break;
                case 'v':
                    sY--;
                    dY[i % 2]--;
                    break;
                case '<':
                    sX--;
                    dX[i % 2]--;
                    break;
            }
            visitedSingleCount += visitedSingle[sX][sY] ? 0 : 1;
            visitedDoubleCount += visitedDouble[dX[i % 2]][dY[i % 2]] ? 0 : 1;
            visitedDouble[dX[i % 2]][dY[i % 2]] = visitedSingle[sX][sY] = true;
        }

        System.out.println(visitedSingleCount);
        System.out.println(visitedDoubleCount);
    }
}
