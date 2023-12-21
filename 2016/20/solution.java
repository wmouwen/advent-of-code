
import java.util.ArrayList;
import java.util.Scanner;

public class AoC_20 {

    class Range {

        long low, high;

        Range(long low, long high) {
            this.low = low;
            this.high = high;
        }
    }

    public void magic() {
        ArrayList<Range> ranges = new ArrayList<>();

        while (sc.hasNextLine()) {
            String[] parts = sc.nextLine().trim().split("-");
            ranges.add(new Range(
                    Long.parseLong(parts[0]),
                    Long.parseLong(parts[1])
            ));
        }

        int count = 0;
        boolean first = true;

        loopRanges:
        for (long i = 0; i <= 4294967295l; i++) {
            for (Range range : ranges) {
                if (range.low <= i && i <= range.high) {
                    i = range.high;
                    continue loopRanges;
                }
            }
            if (first) {
                first = false;
                System.out.println("Part One: " + i);
            }
            count++;
        }

        System.out.println("Part Two: " + count);
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) throws Exception {
        long startTime = System.currentTimeMillis();
        new AoC_20().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}
