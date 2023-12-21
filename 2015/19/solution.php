<?php

$replacements = [];
while (preg_match('/^(\w+)\s=>\s(\w+)$/', trim(fgets(STDIN)), $input)) {
    $replacements[$input[1]][] = $input[2];
}

preg_match_all('/[A-Z][a-z]?/', trim(fgets(STDIN)), $medicine);
$medicine = array_shift($medicine);

$singleReplacementResults = new \Ds\Set;

for ($i = 0; $i < count($medicine); $i++) {
    $original = $medicine[$i];

    foreach (($replacements[$original] ?? []) as $option) {
        $medicine[$i] = $option;
        $singleReplacementResults->add(implode($medicine));
    }

    $medicine[$i] = $original;
}

fwrite(STDOUT, $singleReplacementResults->count() . PHP_EOL);

/**
 * Part Two information:
 *
 * The generated inputs always represent some biology-related chemical component. The symbols Rn, Y and Ar are
 * representing '(', ',' and ')' respectively such that you may read medicine molecule as a series of function calls.
 *
 * Also, the input only contains a few types of replacements:
 *
 *   - A => BC
 *   - A => B(C)
 *   - A => B(C, D)
 *   - A => B(C, D, ...)
 *
 * There are a few rules to these replacements:
 *   - Replacements without brackets always replace a single element by two elements.
 *   - Replacements with brackets always replace a single element by count(comma's) plus two elements, on top of the
 *     comma's and brackets.
 *
 * Using this makes for easy calculation of the amount of steps.
 */

$counts = array_count_values($medicine);

// The base amount of steps needed, n-1
$steps = count($medicine) - 1;

// Brackets are free additions, so don't count them.
$steps -= $counts['Rn'] + $counts['Ar'];

// A comma means both the comma and the following element are extra additions, so don't count them.
$steps -= 2 * $counts['Y'];

fwrite(STDOUT, $steps . PHP_EOL);
