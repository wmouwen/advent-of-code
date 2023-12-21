<?php

const RACE_DURATION = 2503;

class Reindeer
{
    private $speed;
    private $duration;
    private $cycle;

    public function __construct(int $speed, int $duration, int $rest)
    {
        $this->speed    = $speed;
        $this->duration = $duration;
        $this->cycle    = $duration + $rest;
    }

    public function distanceAfter(int $seconds): int
    {
        return $this->speed * (intval($seconds / $this->cycle) * $this->duration + min($seconds % $this->cycle, $this->duration));
    }
}

$reindeers = [];
while (preg_match('/\w+ can fly (\d+) km\/s for (\d+) seconds, but then must rest for (\d+) seconds./', fgets(STDIN), $matches)) {
    $reindeers[] = new Reindeer($matches[1], $matches[2], $matches[3]);
}

$farthest = PHP_INT_MIN;
foreach ($reindeers as $name => $reindeer) {
    $farthest = max($farthest, $reindeer->distanceAfter(RACE_DURATION));
}
fwrite(STDOUT, $farthest . PHP_EOL);

$points   = [];
$farthest = PHP_INT_MIN;
for ($seconds = 1; $seconds <= RACE_DURATION; $seconds++) {
    foreach ($reindeers as $i => $reindeer) {
        $farthest = max($farthest, $reindeer->distanceAfter($seconds));
    }
    foreach ($reindeers as $i => $reindeer) {
        if ($farthest === $reindeer->distanceAfter($seconds)) {
            $points[$i] = ($points[$i] ?? 0) + 1;
        }
    }
}
fwrite(STDOUT, max($points) . PHP_EOL);