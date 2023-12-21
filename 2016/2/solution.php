<?php

const KEYPAD_SIMPLE = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

const KEYPAD_COMPLEX = [
    [null, null, 1, null, null],
    [null, 2, 3, 4, null],
    [5, 6, 7, 8, 9],
    [null, 'A', 'B', 'C', null],
    [null, null, 'D', null, null]
];

function keypad_code(array $keypad, array &$instructions, int $x, int $y): string
{
    $code = "";

    foreach ($instructions as $instruction) {
        foreach ($instruction as $step) {
            $dx = $dy = 0;
            switch ($step) {
                case 'U':
                    $dy--;
                    break;
                case 'D':
                    $dy++;
                    break;
                case 'L':
                    $dx--;
                    break;
                case 'R':
                    $dx++;
                    break;
            }
            if (isset($keypad[$y + $dy][$x + $dx])) {
                $x += $dx;
                $y += $dy;
            }
        }
        $code .= $keypad[$y][$x];
    }

    return $code;
}

$instructions = [];
while ($instruction = trim(fgets(STDIN))) {
    $instructions[] = str_split($instruction);
}

fwrite(STDOUT, keypad_code(KEYPAD_SIMPLE, $instructions, 1, 1) . PHP_EOL);
fwrite(STDOUT, keypad_code(KEYPAD_COMPLEX, $instructions, 0, 2) . PHP_EOL);