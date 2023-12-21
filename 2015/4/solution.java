
import java.math.BigInteger;
import java.security.MessageDigest;
import java.util.Scanner;

public class AoC_04 {

    void magic() throws Exception {
        String input = sc.nextLine().trim();
        long partOne = Long.MAX_VALUE, current = 0;
        
        for (; current <= Long.MAX_VALUE; current++) {
            String md5 = new BigInteger(1, MessageDigest.getInstance("MD5").digest((input + current).getBytes())).toString(16);
            if (md5.length() <= 27) {
                partOne = Math.min(current, partOne);
            }
            if (md5.length() <= 26) {
                break;
            }
        }
        
        System.out.println("Part One: " + partOne);
        System.out.println("Part Two: " + current);
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) throws Exception {
        long startTime = System.currentTimeMillis();
        new AoC_04().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}
