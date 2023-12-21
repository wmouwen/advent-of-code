<?php

$triangles = [];
while ($row = trim(fgets(STDIN))) {
    $triangles[] = explode(' ', preg_replace('/\s+/', ' ', $row));
}

function possible_triangle_count(array $triangles): int
{
    return array_sum(
        array_map(
            function ($triangle) {
                return array_sum($triangle) > 2 * max($triangle);
            },
            $triangles
        )
    );
}

fwrite(STDOUT, possible_triangle_count($triangles) . PHP_EOL);

function transpose(array $input): array
{
    $output = [];
    for ($y = 0; $y < count($input); $y++) {
        for ($x = 0; $x < count($input[$y]); $x++) {
            $output[$x][$y] = $input[$y][$x];
        }
    }

    return $output;
}

$possible = 0;
for ($i = 0; $i < count($triangles); $i += 3) {
    $possible += possible_triangle_count(transpose(array_slice($triangles, $i, 3)));
}

fwrite(STDOUT, $possible . PHP_EOL);