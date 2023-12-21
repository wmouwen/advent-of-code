<?php

const PROGRAMS = 16;
const DANCES   = 1000000000;

function dance(array &$programs, array &$moves): void
{
    foreach ($moves as $move) {
        switch ($move[1]) {
            case 's':
                $programs = array_merge(
                    array_slice($programs, -1 * $move[2]),
                    array_slice($programs, 0, PROGRAMS - $move[2])
                );
                break;
            case 'x':
                $tmp                = $programs[$move[2]];
                $programs[$move[2]] = $programs[$move[4]];
                $programs[$move[4]] = $tmp;
                break;
            case 'p':
                $tmp          = $programs[$a = array_search($move[2], $programs)];
                $programs[$a] = $programs[$b = array_search($move[4], $programs)];
                $programs[$b] = $tmp;
                break;
        }
    }
}

for ($i = 0; $i < PROGRAMS; $i++) {
    $programs[$i] = chr(ord('a') + $i);
}
preg_match_all("/(s|x|p)([a-p0-9]{1,2})(\/([a-p0-9]{1,2}))?/", trim(fgets(STDIN)), $moves, PREG_SET_ORDER);

dance($programs, $moves);
fwrite(STDOUT, implode($programs) . PHP_EOL);

$max = DANCES;
for ($i = 2; $i <= $max; $i++) {
    dance($programs, $moves);

    $test = array_merge($programs);
    sort($test);
    if (implode($test) == implode($programs)) {
        $max = (DANCES % $i);
        $i   = 0;
        continue;
    }
}
fwrite(STDOUT, implode($programs) . PHP_EOL);