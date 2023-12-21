<?php

$input = trim(fgets(STDIN));
$five  = $six = 0;

for ($i = 1; !$six; $i++) {
    if (!$five && strpos(md5($input . $i), '00000') === 0) {
        fwrite(STDOUT, ($five = $i) . PHP_EOL);
    }
    if (!$six && strpos(md5($input . $i), '000000') === 0) {
        fwrite(STDOUT, ($six = $i) . PHP_EOL);
    }
}

