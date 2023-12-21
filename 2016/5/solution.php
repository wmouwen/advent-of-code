<?php

$hits_left    = 8;
$password_one = [];
$password_two = array_fill(0, $hits_left, null);

for ($i = 0, $door_id = trim(fgets(STDIN)); $hits_left; $i++) {
    $md5 = md5($door_id . $i);

    if (substr($md5, 0, 5) === '00000') {
        if (count($password_one) < 8) {
            $password_one[] = $md5[5];
        }

        if (preg_match('/^[0-7]$/', $md5[5]) && is_null($password_two[intval($md5[5])])) {
            $password_two[intval($md5[5])] = $md5[6];
            $hits_left--;
        }
    }
}

fwrite(STDOUT, implode($password_one) . PHP_EOL);
fwrite(STDOUT, implode($password_two) . PHP_EOL);