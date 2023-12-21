<?php

class Star
{
    public $x;
    public $y;
    public $dx;
    public $dy;

    public function __construct(int $x, int $y, int $dx, int $dy)
    {
        $this->x = $x;
        $this->y = $y;
        $this->dx = $dx;
        $this->dy = $dy;
    }

    public function forward(): void
    {
        $this->x += $this->dx;
        $this->y += $this->dy;
    }

    public function reverse(): void
    {
        $this->x -= $this->dx;
        $this->y -= $this->dy;
    }
}

class Sky
{
    public $stars = [];

    public function addStar(Star $star): void
    {
        $this->stars[] = $star;
    }

    public function forward(): void
    {
        foreach ($this->stars as $star) {
            $star->forward();
        }
    }

    public function reverse(): void
    {
        foreach ($this->stars as $star) {
            $star->reverse();
        }
    }

    public function box(): array
    {
        $minx = PHP_INT_MAX;
        $maxx = PHP_INT_MIN;
        $miny = PHP_INT_MAX;
        $maxy = PHP_INT_MIN;

        foreach ($this->stars as $star) {
            $minx = min($minx, $star->x);
            $maxx = max($maxx, $star->x);
            $miny = min($miny, $star->y);
            $maxy = max($maxy, $star->y);
        }

        return [$minx, $maxx, $miny, $maxy];
    }

    public function boxSize(): int
    {
        [$minx, $maxx, $miny, $maxy] = $this->box();
        return ($maxx - $minx) * ($maxy - $miny);
    }

    public function __toString(): string
    {
        [$minx, $maxx, $miny, $maxy] = $this->box();

        $grid = array_fill($miny, $maxy - $miny + 1, array_fill($minx, $maxx - $minx + 1, '.'));

        foreach ($this->stars as $star) {
            $grid[$star->y][$star->x] = '#';
        }

        return implode(PHP_EOL, array_map('implode', $grid));
    }
}

$sky = new Sky;

while (preg_match('/^position=<\s*?(-?\d+),\s*?(-?\d+)> velocity=<\s*?(-?\d+),\s*?(-?\d+)>$/', trim(fgets(STDIN)), $input)) {
    $sky->addStar(new Star($input[1], $input[2], $input[3], $input[4]));
}

$time = 0;
$boxSize = PHP_INT_MAX;

do {
    $time++;

    $previousSize = $boxSize;
    $sky->forward();
    $boxSize = $sky->boxSize();
} while ($boxSize < $previousSize);

$sky->reverse();
$time--;

fwrite(STDOUT, $sky . PHP_EOL);
fwrite(STDOUT, $time . PHP_EOL);
