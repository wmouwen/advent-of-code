import java.util.Scanner;

public class IWasToldThereWouldBeNoMath {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) throws Exception {
        long surface = 0, ribbon = 0;

        while (sc.hasNextLine()) {
            String[] input = sc.nextLine().trim().split("x");
            int x = Integer.parseInt(input[0]), y = Integer.parseInt(input[1]), z = Integer.parseInt(input[2]);
            int a = x * y, b = x * z, c = y * z;

            surface += 2 * (a + b + c) + Math.min(a, Math.min(b, c));
            ribbon += x * y * z + 2 * (x + y + z - Math.max(x, Math.max(y, z)));
        }

        System.out.println(surface);
        System.out.println(ribbon);
    }
}
