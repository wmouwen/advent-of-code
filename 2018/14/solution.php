<?php

ini_set('memory_limit', '4G');

$input = trim(fgets(STDIN));
$intput = intval($input);
$lenput = strlen($input);
$powput = pow(10, $lenput);

$scores = [3, 7];
$sequence = 37;

$elfA = 0;
$elfB = 1;

$recipesBeforeSequence = null;

while (count($scores) < $intput + 10 || $recipesBeforeSequence === null) {
    $sum = $scores[$elfA] + $scores[$elfB];

    if ($sum >= 10) {
        $scores[] = 1;
        $sequence = ((10 * $sequence) % $powput) + 1;

        if ($sequence === $intput) {
            $recipesBeforeSequence = $recipesBeforeSequence ?? count($scores) - $lenput;
        }
    }

    $modten = $sum % 10;
    $scores[] = $modten;
    $sequence = ((10 * $sequence) % $powput) + $modten;

    if ($sequence === $intput) {
        $recipesBeforeSequence = $recipesBeforeSequence ?? count($scores) - $lenput;
    }

    $elfA = ($elfA + $scores[$elfA] + 1) % count($scores);
    $elfB = ($elfB + $scores[$elfB] + 1) % count($scores);
}

fwrite(STDOUT, implode(array_splice($scores, $intput, 10)) . PHP_EOL);
fwrite(STDOUT, $recipesBeforeSequence . PHP_EOL);
