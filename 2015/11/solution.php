<?php

function next_password(string &$password): string
{
    do {
        for ($i = strlen($password) - 1; ; $i--) {
            $password[$i] = chr(((ord($password[$i]) - 18) % 26) + 97);
            if ($password[$i] !== 'a') {
                break;
            }
        }

        $straight = false;
        $in_pair  = false;
        $pairs    = [];
        for ($i = 0; $i < strlen($password); $i++) {
            $straight |= $i >= 2
                && ord($password[$i]) == ord($password[$i - 1]) + 1
                && ord($password[$i]) == ord($password[$i - 2]) + 2;

            if ($in_pair = !$in_pair && $i >= 1 && $password[$i] == $password[$i - 1]) {
                $pairs = array_unique(array_merge($pairs, [$password[$i]]));
            }
        }
    } while (!$straight || preg_match('/(i|o|l)/', $password) || count($pairs) < 2);

    return $password;
}

$password = trim(fgets(STDIN));
fwrite(STDOUT, next_password($password) . PHP_EOL);
fwrite(STDOUT, next_password($password) . PHP_EOL);
