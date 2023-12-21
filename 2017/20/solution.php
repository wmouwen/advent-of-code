<?php

class Particle
{
    private $id = 0;
    private $position = [];
    private $velocity = [];
    private $acceleration = [];
    private $destroying = false;
    private $destroyed = false;

    public function __construct(int $id, array $position, array $velocity, array $acceleration)
    {
        $this->id           = $id;
        $this->position     = $position;
        $this->velocity     = $velocity;
        $this->acceleration = $acceleration;
    }

    public function move(): void
    {
        $this->destroyed   = $this->destroying;
        $this->velocity[0] += $this->acceleration[0];
        $this->velocity[1] += $this->acceleration[1];
        $this->velocity[2] += $this->acceleration[2];
        $this->position[0] += $this->velocity[0];
        $this->position[1] += $this->velocity[1];
        $this->position[2] += $this->velocity[2];
    }

    public function destroy(): void
    {
        $this->destroying = true;
    }

    public function detectCollisionWith(Particle &$other): void
    {
        $pos = $other->getPosition();
        if ($this->position[0] === $pos[0] && $this->position[1] === $pos[1] && $this->position[2] === $pos[2]) {
            $this->destroy();
            $other->destroy();
        }
    }

    public function getID(): int
    {
        return $this->id;
    }

    public function getPosition(): array
    {
        return $this->position;
    }

    public function getDistance(): int
    {
        return abs($this->position[0]) + abs($this->position[1]) + abs($this->position[2]);
    }

    public function isDestroyed(): bool
    {
        return $this->destroyed;
    }
}

$particles = [];

$id = 0;
while ($line = fgets(STDIN)) {
    preg_match('/p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>/', $line, $matches);
    $matches     = array_map('intval', $matches);
    $particles[] = new Particle($id++,
        [$matches[1], $matches[2], $matches[3]],
        [$matches[4], $matches[5], $matches[6]],
        [$matches[7], $matches[8], $matches[9]]
    );
}

for ($cycle = 0; $cycle < 400; $cycle++) {
    foreach ($particles as $particle) {
        $particle->move();
        if (!$particle->isDestroyed()) {
            foreach ($particles as $other) {
                if (!$other->isDestroyed() && $particle->getID() !== $other->getID()) {
                    $particle->detectCollisionWith($other);
                }
            }
        }
    }
}

$count = 0;
foreach ($particles as $particle) {
    if (!$particle->isDestroyed()) {
        $count++;
    }
}

usort($particles, function (Particle &$a, Particle &$b) {
    return $a->getDistance() <=> $b->getDistance();
});

fwrite(STDOUT, $particles[0]->getID() . PHP_EOL);
fwrite(STDOUT, $count . PHP_EOL);