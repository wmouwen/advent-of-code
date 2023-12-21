
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class AoC_12 {

    void magic() throws Exception {
        String input = sc.nextLine();
        long total = 0;
        for (Matcher matcher = Pattern.compile("-?\\d+").matcher(input); matcher.find();) {
            total += Integer.valueOf(matcher.group());
        }
        System.out.println("Part One: " + total);
        System.out.println("Part Two: " + recurseJSON(new JSONParser().parse(input)));
    }

    long recurseJSON(Object input) throws Exception {
        boolean isStructure = input.toString().charAt(0) == '{';
        long total = 0;
        for (Object obj : isStructure ? ((JSONObject) input).values() : (JSONArray) input) {
            switch (obj.toString().charAt(0)) {
                case '[':
                case '{':
                    total += recurseJSON(obj);
                    break;
                default:
                    try {
                        total += Integer.parseInt(obj.toString());
                    } catch (Exception e) {
                        if (isStructure && obj.toString().equals("red")) {
                            return 0l;
                        }
                    }
            }
        }
        return total;
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) throws Exception {
        long startTime = System.currentTimeMillis();
        new AoC_12().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}
