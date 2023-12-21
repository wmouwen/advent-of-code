<?php

const LETTERS_IN_HEX = [
    0x19297A52 => 'A',
    0x392E4A5C => 'B',
    0x1928424C => 'C',
    0x39294A5C => 'D',
    0x3D0E421E => 'E',
    0x3D0E4210 => 'F',
    0x19285A4E => 'G',
    0x252F4A52 => 'H',
    0x1C42108E => 'I',
    0x0C210A4C => 'J',
    0x254C5292 => 'K',
    0x2108421E => 'L',
    // Unknown => 'M',
    // Unknown => 'N',
    0x19294A4C => 'O',
    0x39297210 => 'P',
    // Unknown => 'Q',
    0x39297292 => 'R',
    0x1D08305C => 'S',
    0x1C421084 => 'T',
    0x25294A4C => 'U',
    // Unknown => 'V',
    // Unknown => 'W',
    // Unknown => 'X',
    0x23151084 => 'Y',
    0x3C22221E => 'Z'
];

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

function rotate(array $input, int $shift): array
{
    $output = [];
    for ($x = 0; $x < count($input); $x++) {
        $output[($x + $shift) % count($input)] = $input[$x];
    }

    return $output;
}

function pixels_to_letter(array $pixels): string
{
    return LETTERS_IN_HEX[bindec(implode(array_map('implode', $pixels)))] ?? "?";
}

$screen = array_fill(0, 6, array_fill(0, 50, 0));

while (preg_match('/^(rect|rotate) ((\d+)x(\d+)|(row|column) \w=(\d+) by (\d+))$/', trim(fgets(STDIN)), $instruction)) {
    if ($instruction[1] === 'rect') {
        for ($y = 0; $y < intval($instruction[4]); $y++) {
            for ($x = 0; $x < intval($instruction[3]); $x++) {
                $screen[$y][$x] = 1;
            }
        }
    } else { // rotate
        if ($instruction[5] === 'column') {
            $screen = transpose($screen);
        }
        $screen[$instruction[6]] = rotate($screen[$instruction[6]], $instruction[7]);
        if ($instruction[5] === 'column') {
            $screen = transpose($screen);
        }
    }
}

fwrite(STDOUT, array_sum(array_map('array_sum', $screen)) . PHP_EOL);

$letters = [];
for ($i = 0; $i < count($screen[0]); $i += 5) {
    $letters[] = pixels_to_letter(array_map(function ($row) use ($i) {
        return array_splice($row, $i, 5);
    }, $screen));
}

fwrite(STDOUT, implode($letters) . PHP_EOL);