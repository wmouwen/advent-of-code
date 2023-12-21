import java.util.Scanner;

public class NotQuiteLisp {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) throws Exception {
        char[] input = sc.nextLine().trim().toCharArray();
        int floor = 0, basement = 0;

        for (int i = 0; i < input.length; i++) {
            floor += input[i] == '(' ? 1 : -1;
            if (floor == -1 && basement == 0) {
                basement = i + 1;
            }
        }

        System.out.println(floor);
        System.out.println(basement);
    }
}
