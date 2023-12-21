<?php

function knot_hash(string $input): array
{
    $lengths     = array_merge(array_map('ord', str_split($input)), [17, 31, 73, 47, 23]);
    $hash_sparse = range(0, 255);

    for ($position = $skip = 0, $rounds = 64; $rounds; $rounds--) {
        foreach ($lengths as $length) {
            for ($i = 0; 2 * $i < $length; $i++) {
                $tmp             = $hash_sparse[$a = ($position + $i) % count($hash_sparse)];
                $hash_sparse[$a] = $hash_sparse[$b = ($position + min($length, count($hash_sparse) - 1) - 1 - $i) % count($hash_sparse)];
                $hash_sparse[$b] = $tmp;
            }
            $position = ($position + $length + $skip++) % count($hash_sparse);
        }
    }

    $hash_dense = array_fill(0, 16, 0);
    for ($block = 0; $block < 16; $block++) {
        for ($sub = 0; $sub < 16; $sub++) {
            $hash_dense[$block] ^= $hash_sparse[16 * $block + $sub];
        }
    }

    return $hash_dense;
}

function recurse_set_false(array &$grid, $x, $y)
{
    $grid[$x][$y] = false;
    foreach ([[-1, 0], [1, 0], [0, -1], [0, 1]] as $d) {
        if ($grid[$x + $d[0]][$y + $d[1]] ?? false) {
            recurse_set_false($grid, $x + $d[0], $y + $d[1]);
        }
    }
}

$input              = trim(fgets(STDIN));
$hamming_weight_sum = 0;
$grid               = array_fill(0, 128, []);

for ($y = 0; $y < 128; $y++) {
    $hash = knot_hash($input . '-' . $y);
    for ($x = 0; $x < count($hash); $x++) {
        for ($dx = 7; $hash[$x]; $hash[$x] >>= 1, $dx--) {
            $grid[8 * $x + $dx][$y] = ($hash[$x] & 1) ? true : false;
            $hamming_weight_sum     += $hash[$x] & 1;
        }
    }
}
fwrite(STDOUT, $hamming_weight_sum . PHP_EOL);

$regions = 0;
for ($y = 0; $y < 128; $y++) {
    for ($x = 0; $x < 128; $x++) {
        if ($grid[$x][$y] ?? false) {
            $regions++;
            recurse_set_false($grid, $x, $y);
        }
    }
}
fwrite(STDOUT, $regions . PHP_EOL);