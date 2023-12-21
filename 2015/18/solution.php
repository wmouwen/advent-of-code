<?php

class GameOfLife
{
    private $universe = [];

    public function addRow(string $cells): void
    {
        $this->universe[] = array_map(function ($cell) {
            return $cell === '#';
        }, str_split($cells));
    }

    public function evolve(): void
    {
        $previous = $this->universe;

        for ($y = 0; $y < count($this->universe); $y++) {
            for ($x = 0; $x < count($this->universe[$y]); $x++) {
                $sum = 0;
                for ($dy = -1; $dy <= 1; $dy++) {
                    for ($dx = -1; $dx <= 1; $dx++) {
                        if ($dy !== 0 || $dx !== 0) {
                            $sum += $previous[$y + $dy][$x + $dx] ?? 0;
                        }
                    }
                }
                $this->universe[$y][$x] = ($previous[$y][$x] && $sum === 2) || $sum === 3;
            }
        }
    }

    public function lightCorners(): void
    {
        foreach ([&$this->universe[0], &$this->universe[count($this->universe) - 1]] as &$row) {
            $row[0] = $row[count($row) - 1] = true;
        }
    }

    public function alive(): int
    {
        return array_sum(array_map('array_sum', $this->universe));
    }
}

$game_of_life_one = new GameOfLife();
$game_of_life_two = new GameOfLife();

while ($row = trim(fgets(STDIN))) {
    $game_of_life_one->addRow($row);
    $game_of_life_two->addRow($row);
}

for ($cycle = 100, $game_of_life_two->lightCorners(); $cycle--; $game_of_life_two->lightCorners()) {
    $game_of_life_one->evolve();
    $game_of_life_two->evolve();
}

fwrite(STDOUT, $game_of_life_one->alive() . PHP_EOL);
fwrite(STDOUT, $game_of_life_two->alive() . PHP_EOL);