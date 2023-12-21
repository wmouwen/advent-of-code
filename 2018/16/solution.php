<?php

$functions = [
    'addr' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $registers[$a] + $registers[$b];
        return $registers;
    },
    'addi' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $registers[$a] + $b;
        return $registers;
    },
    'mulr' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $registers[$a] * $registers[$b];
        return $registers;
    },
    'muli' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $registers[$a] * $b;
        return $registers;
    },
    'banr' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $registers[$a] & $registers[$b];
        return $registers;
    },
    'bani' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $registers[$a] & $b;
        return $registers;
    },
    'borr' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $registers[$a] | $registers[$b];
        return $registers;
    },
    'bori' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $registers[$a] | $b;
        return $registers;
    },
    'setr' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $registers[$a];
        return $registers;
    },
    'seti' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $a;
        return $registers;
    },
    'gtir' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $a > $registers[$b] ? 1 : 0;
        return $registers;
    },
    'gtri' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $registers[$a] > $b ? 1 : 0;
        return $registers;
    },
    'gtrr' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $registers[$a] > $registers[$b] ? 1 : 0;
        return $registers;
    },
    'eqir' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $a === $registers[$b] ? 1 : 0;
        return $registers;
    },
    'eqri' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $registers[$a] === $b ? 1 : 0;
        return $registers;
    },
    'eqrr' => function (int $a, int $b, int $c, array $registers): array {
        $registers[$c] = $registers[$a] === $registers[$b] ? 1 : 0;
        return $registers;
    },
];

$ambiguous = 0;

$opcodes = array_fill(0, count($functions), array_keys($functions));

while (preg_match('/Before:\s+\[(\d+),\s+(\d+),\s+(\d+),\s+(\d+)\]/', fgets(STDIN), $before)) {
    array_shift($before);
    $before = array_map('intval', $before);

    preg_match('/(\d+)\s+(\d+)\s+(\d+)\s+(\d+)/', fgets(STDIN), $instruction);
    $opcode = intval($instruction[1]);
    $a = intval($instruction[2]);
    $b = intval($instruction[3]);
    $c = intval($instruction[4]);

    preg_match('/After:\s+\[(\d+),\s+(\d+),\s+(\d+),\s+(\d+)\]/', fgets(STDIN), $after);
    array_shift($after);
    $after = array_map('intval', $after);

    fgets(STDIN); // Catch blank line.

    // Find out the possible functions for each observation.
    $possibilities = [];
    foreach ($functions as $name => $function) {
        if ($function($a, $b, $c, $before) === $after) {
            $possibilities[] = $name;
        }
    }

    if (count($possibilities) >= 3) {
        $ambiguous++;
    }

    // Deduce what functions are possible for each opcode.
    $opcodes[$opcode] = array_intersect($opcodes[$opcode], $possibilities);
}

fwrite(STDOUT, $ambiguous . PHP_EOL);

// Matrix sweeping over opcodes and their possibilities.
do {
    foreach ($opcodes as $opcode => $possibilities) {
        if (count($possibilities) === 1) {
            $needle = reset($possibilities);
            foreach (array_keys($opcodes) as $other) {
                $index = array_search($needle, $opcodes[$other]);
                if ($opcode !== $other && $index !== false) {
                    unset($opcodes[$other][$index]);
                }
            }
        }
    }
} while (array_reduce($opcodes, function ($carry, $possibilities) {
    return $carry + count($possibilities);
}, 0) > count($functions));

$opcodes = array_map(function ($possibilities) {
    return reset($possibilities);
}, $opcodes);

// Catch additional blank line.
fgets(STDIN);

// Execute program.
$registers = array_fill(0, 4, 0);

while (preg_match('/(\d+)\s+(\d+)\s+(\d+)\s+(\d+)/', fgets(STDIN), $instruction)) {
    $opcode = intval($instruction[1]);
    $a = intval($instruction[2]);
    $b = intval($instruction[3]);
    $c = intval($instruction[4]);

    $registers = $functions[$opcodes[$opcode]]($a, $b, $c, $registers);
}

fwrite(STDOUT, $registers[0] . PHP_EOL);
