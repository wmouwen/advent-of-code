<?php

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

class Rule
{
    private $horizontal = '';
    private $vertical = '';
    private $count = 0;
    private $replacement = [];

    function __construct(string $match, string $replacement)
    {
        $this->horizontal  = str_replace('/', '', $match);
        $this->vertical    = implode(array_map('implode', transpose(array_map('str_split', explode('/', $match)))));
        $this->count       = substr_count($this->horizontal, '#');
        $this->replacement = explode('/', $replacement);
    }

    public function test(array $square): bool
    {
        if (substr_count(implode($square), '#') !== $this->count) {
            return false;
        }

        if ($this->matches(implode($square)) || $this->matches(implode(array_reverse($square)))) {
            return true;
        }

        $square = array_map('strrev', $square);
        if ($this->matches(implode($square)) || $this->matches(implode(array_reverse($square)))) {
            return true;
        }

        return false;
    }

    private function matches(string $test): bool
    {
        return $this->horizontal === $test || $this->vertical === $test;
    }

    public function getReplacement(): array
    {
        return $this->replacement;
    }
}

$picture   = explode('/', '.#./..#/###');
$rules_2x2 = [];
$rules_3x3 = [];

while ($line = fgets(STDIN)) {
    $explode = explode(' ', trim($line));
    if (strlen($explode[0]) == 5) {
        $rules_2x2[] = new Rule($explode[0], $explode[2]);
    } else {
        $rules_3x3[] = new Rule($explode[0], $explode[2]);
    }
}

$part_one = null;

for ($i = 1; $i <= 18; ++$i) {
    $new = [];

    if ((count($picture) % 2) == 0) {
        $squares = count($picture) / 2;
        for ($y = 0; $y < $squares; $y++) {
            for ($x = 0; $x < $squares; $x++) {
                $square = [
                    substr($picture[2 * $y + 0], 2 * $x, 2),
                    substr($picture[2 * $y + 1], 2 * $x, 2)
                ];
                foreach ($rules_2x2 as $rule) {
                    if ($rule->test($square)) {
                        $replacement     = $rule->getReplacement();
                        $new[3 * $y + 0] = ($new[3 * $y + 0] ?? '') . $replacement[0];
                        $new[3 * $y + 1] = ($new[3 * $y + 1] ?? '') . $replacement[1];
                        $new[3 * $y + 2] = ($new[3 * $y + 2] ?? '') . $replacement[2];
                        break;
                    }
                }
            }
        }
    } else {
        $squares = count($picture) / 3;
        for ($y = 0; $y < $squares; $y++) {
            for ($x = 0; $x < $squares; $x++) {
                $square = [
                    substr($picture[3 * $y + 0], 3 * $x, 3),
                    substr($picture[3 * $y + 1], 3 * $x, 3),
                    substr($picture[3 * $y + 2], 3 * $x, 3)
                ];
                foreach ($rules_3x3 as $rule) {
                    if ($rule->test($square)) {
                        $replacement     = $rule->getReplacement();
                        $new[4 * $y + 0] = ($new[4 * $y + 0] ?? '') . $replacement[0];
                        $new[4 * $y + 1] = ($new[4 * $y + 1] ?? '') . $replacement[1];
                        $new[4 * $y + 2] = ($new[4 * $y + 2] ?? '') . $replacement[2];
                        $new[4 * $y + 3] = ($new[4 * $y + 3] ?? '') . $replacement[3];
                        break;
                    }
                }
            }
        }
    }

    $picture = $new;

    if ($i == 5) {
        fwrite(STDOUT, substr_count(implode($picture), '#') . PHP_EOL);
    }
}

fwrite(STDOUT, substr_count(implode($picture), '#') . PHP_EOL);