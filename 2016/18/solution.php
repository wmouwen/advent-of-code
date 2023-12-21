<?php

$row   = array_map('intval', str_split(strtr(trim(fgets(STDIN)), '.^', '10')));
$count = array_sum($row);

for ($i = 2; $i <= 400000; $i++) {

    $previous = $row;
    for ($c = 0; $c < count($previous); $c++) {
        $row[$c] = in_array(
            4 * ($previous[$c - 1] ?? 1) + 2 * $previous[$c] + ($previous[$c + 1] ?? 1),
            [6, 3, 4, 1]
        ) ? 0 : 1;
    }

    $count += array_sum($row);

    if ($i === 40) {
        fwrite(STDOUT, $count . PHP_EOL);
    }
}

fwrite(STDOUT, $count . PHP_EOL);
