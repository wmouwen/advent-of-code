<?php

const OPEN_DOORS = ['b', 'c', 'd', 'e', 'f'];

$salt  = trim(fgets(STDIN));
$max   = PHP_INT_MIN;
$min   = null;
$queue = [[0, 0, '']];

while ($step = array_shift($queue)) {
    if ($step[0] === 3 && $step[1] === 3) {
        $max = max($max, strlen($step[2]));

        if (strlen($step[2]) <= strlen($min ?? $step[2])) {
            $min = $step[2];
        }
        
    } else {
        $md5 = md5($salt . $step[2]);

        if ($step[1] > 0 && in_array($md5[0], OPEN_DOORS)) {
            $queue[] = [$step[0], $step[1] - 1, $step[2] . 'U'];
        }
        if ($step[1] < 3 && in_array($md5[1], OPEN_DOORS)) {
            $queue[] = [$step[0], $step[1] + 1, $step[2] . 'D'];
        }
        if ($step[0] > 0 && in_array($md5[2], OPEN_DOORS)) {
            $queue[] = [$step[0] - 1, $step[1], $step[2] . 'L'];
        }
        if ($step[0] < 3 && in_array($md5[3], OPEN_DOORS)) {
            $queue[] = [$step[0] + 1, $step[1], $step[2] . 'R'];
        }
    }
}

fwrite(STDOUT, $min . PHP_EOL);
fwrite(STDOUT, $max . PHP_EOL);