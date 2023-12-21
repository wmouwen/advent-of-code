<?php

function knot_hash_sparse(array $lengths, int $rounds = 64): array
{
    $hash = range(0, 255);

    for ($position = $skip = 0; $rounds; $rounds--) {
        foreach ($lengths as $length) {
            for ($i = 0; 2 * $i < $length; $i++) {
                $tmp      = $hash[$a = ($position + $i) % count($hash)];
                $hash[$a] = $hash[$b = ($position + min($length, count($hash) - 1) - 1 - $i) % count($hash)];
                $hash[$b] = $tmp;
            }
            $position = ($position + $length + $skip++) % count($hash);
        }
    }

    return $hash;
}

$hash_sparse = knot_hash_sparse(array_map('intval', explode(',', $input = trim(fgets(STDIN)))), 1);

fwrite(STDOUT, $hash_sparse[0] * $hash_sparse[1] . PHP_EOL);

$hash_sparse = knot_hash_sparse(array_merge(array_map('ord', str_split($input)), [17, 31, 73, 47, 23]));
$hash_dense  = array_fill(0, 16, 0);

for ($block = 0; $block < 16; $block++) {
    for ($sub = 0; $sub < 16; $sub++) {
        $hash_dense[$block] ^= $hash_sparse[16 * $block + $sub];
    }
    $hash_dense[$block] = str_pad(dechex($hash_dense[$block]), 2, '0', STR_PAD_LEFT);
}

fwrite(STDOUT, implode($hash_dense) . PHP_EOL);