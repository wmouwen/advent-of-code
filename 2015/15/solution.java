
import java.util.ArrayList;
import java.util.Scanner;

public class AoC_15 {

    class Ingredient {

        long capacity, durability, flavor, texture, calories, usage;

        Ingredient(String[] input) {
            capacity = Integer.valueOf(input[2].substring(0, input[2].length() - 1));
            durability = Integer.valueOf(input[4].substring(0, input[4].length() - 1));
            flavor = Integer.valueOf(input[6].substring(0, input[6].length() - 1));
            texture = Integer.valueOf(input[8].substring(0, input[8].length() - 1));
            calories = Integer.valueOf(input[10]);
        }
    }

    void magic() {
        ArrayList<Ingredient> ingredients = new ArrayList<>();
        while (sc.hasNextLine()) {
            ingredients.add(new Ingredient(sc.nextLine().split(" ")));
        }
        System.out.println("Part One: " + recurse(ingredients, 0, 0, false));
        System.out.println("Part Two: " + recurse(ingredients, 0, 0, true));
    }

    long recurse(ArrayList<Ingredient> ingredients, int used, int depth, boolean limitCalories) {
        if (depth == ingredients.size()) {
            long capacity = 0, durability = 0, flavor = 0, texture = 0, calories = 0;
            for (Ingredient ing : ingredients) {
                capacity += ing.capacity * ing.usage;
                durability += ing.durability * ing.usage;
                flavor += ing.flavor * ing.usage;
                texture += ing.texture * ing.usage;
                calories += ing.calories * ing.usage;
            }
            if (used != 100 || capacity < 0 || durability < 0 || flavor < 0 || texture < 0 || (limitCalories && calories != 500l)) {
                return 0l;
            }
            return capacity * durability * flavor * texture;
        }
        long max = 0l;
        for (int i = 100 - used; i >= 0; i--) {
            ingredients.get(depth).usage = i;
            max = Math.max(max, recurse(ingredients, used + i, depth + 1, limitCalories));
        }
        return max;
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_15().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}
