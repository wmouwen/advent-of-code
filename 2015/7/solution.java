
import java.util.HashMap;
import java.util.Scanner;

public class AoC_07 {

    enum Logic {

        AND, OR, NOT, RSHIFT, LSHIFT, DIRECT;

        final static int WIDTH = 0xFFFF;

        int output(int[] input) {
            switch (this) {
                case AND:
                    return input[0] & input[1];
                case OR:
                    return input[0] | input[1];
                case NOT:
                    return (~input[0]) & WIDTH;
                case LSHIFT:
                    return (input[0] << input[1]) & WIDTH;
                case RSHIFT:
                    return input[0] >> input[1];
                default:
                    return input[0];
            }
        }
    };

    class Circuit {

        HashMap<String, Gate> gates = new HashMap<>();

        Gate getGate(String wireName) {
            if (!gates.containsKey(wireName)) {
                gates.put(wireName, new Gate());
            }
            return gates.get(wireName);
        }

        class Gate {

            Logic logic = null;
            Gate[] inputs;
            int[] inputValues;

            int getOutput() {
                for (int i = 0; i < inputValues.length; i++) {
                    if (inputValues[i] == -1 && inputs[i] != null) {
                        inputValues[i] = inputs[i].getOutput();
                    }
                }
                return logic.output(inputValues);
            }

            void setInput(String[] data) {
                inputs = new Gate[data.length];
                inputValues = new int[data.length];
                for (int i = 0; i < data.length; i++) {
                    try {
                        inputValues[i] = Integer.parseInt(data[i]);
                    } catch (Exception e) {
                        inputs[i] = getGate(data[i]);
                        inputValues[i] = -1;
                    }
                }
            }

            void reset() {
                for (int i = 0; i < inputValues.length; i++) {
                    inputValues[i] = inputs[i] != null ? -1 : inputValues[i];
                }
            }
        }
    }

    void magic() {
        Circuit circuit = new Circuit();
        while (sc.hasNextLine()) {
            String[] input = sc.nextLine().split(" ");
            Circuit.Gate gate = circuit.getGate(input[input.length - 1]);
            switch (input.length) {
                case 3:
                    gate.logic = Logic.DIRECT;
                    gate.setInput(new String[]{input[0]});
                    break;
                case 4:
                    gate.logic = Logic.NOT;
                    gate.setInput(new String[]{input[1]});
                    break;
                default:
                    gate.logic = Logic.valueOf(input[1]);
                    gate.setInput(new String[]{input[0], input[2]});
                    break;
            }
        }
        Circuit.Gate a = circuit.getGate("a");
        System.out.println("Part One: " + a.getOutput());

        Circuit.Gate b = circuit.getGate("b");
        b.inputs = new Circuit.Gate[1];
        b.inputValues = new int[]{a.getOutput()};
        b.logic = Logic.DIRECT;
        for (Circuit.Gate gate : circuit.gates.values()) {
            gate.reset();
        }
        System.out.println("Part Two: " + a.getOutput());
    }

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        new AoC_07().magic();
        System.out.println("Running time: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}

