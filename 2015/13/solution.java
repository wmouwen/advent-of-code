
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class AoC_13 {

    class Person {

        HashMap<String, Integer> likes = new HashMap<>();
    }

    void magic() {
        HashMap<String, Person> persons = new HashMap<>();

        while (sc.hasNextLine()) {
            String[] input = sc.nextLine().split(" ");
            if (!persons.containsKey(input[0])) {
                persons.put(input[0], new Person());
            }
            persons.get(input[0]).likes.put(
                    input[10].substring(0, input[10].length() - 1),
                    (input[2].equals("lose") ? -1 : 1) * Integer.valueOf(input[3])
            );
        }
        System.out.println("Part One: "
                + findOptimalSeating(persons, new String[persons.size()], new ArrayList<String>()));

        String myName = "Willem";
        persons.put(myName, new Person());
        for (String otherName : persons.keySet()) {
            if (!otherName.equals(myName)) {
                persons.get(otherName).likes.put(myName, 0);
                persons.get(myName).likes.put(otherName, 0);
            }
        }
        System.out.println("Part Two: "
                + findOptimalSeating(persons, new String[persons.size()], new ArrayList<String>()));
    }

    int findOptimalSeating(HashMap<String, Person> persons, String[] seating, ArrayList<String> seated) {
        int maxHappiness = 0;
        if (seated.size() == seating.length) {
            for (int i = 0; i < seating.length; i++) {
                maxHappiness += persons.get(seating[i]).likes.get(seating[(i + 1) % seating.length])
                        + persons.get(seating[(i + 1) % seating.length]).likes.get(seating[i]);
            }
            return maxHappiness;
        }
        for (String person : persons.keySet()) {
            if (!seated.contains(person)) {
                seating[seated.size()] = person;
                seated.add(person);
                maxHappiness = Math.max(maxHappiness, findOptimalSeating(persons, seating, seated));
                seated.remove(person);
            }
        }
        return maxHappiness;
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_13().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}
