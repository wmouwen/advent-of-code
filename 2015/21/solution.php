<?php

const WEAPONS = [
    ['cost' => 8, 'damage' => 4, 'armor' => 0],
    ['cost' => 10, 'damage' => 5, 'armor' => 0],
    ['cost' => 25, 'damage' => 6, 'armor' => 0],
    ['cost' => 40, 'damage' => 7, 'armor' => 0],
    ['cost' => 74, 'damage' => 8, 'armor' => 0]
];

const ARMOR = [
    ['cost' => 0, 'damage' => 0, 'armor' => 0],
    ['cost' => 13, 'damage' => 0, 'armor' => 1],
    ['cost' => 31, 'damage' => 0, 'armor' => 2],
    ['cost' => 53, 'damage' => 0, 'armor' => 3],
    ['cost' => 75, 'damage' => 0, 'armor' => 4],
    ['cost' => 102, 'damage' => 0, 'armor' => 5]
];

const RINGS = [
    ['cost' => 0, 'damage' => 0, 'armor' => 0],
    ['cost' => 0, 'damage' => 0, 'armor' => 0],
    ['cost' => 25, 'damage' => 1, 'armor' => 0],
    ['cost' => 50, 'damage' => 2, 'armor' => 0],
    ['cost' => 100, 'damage' => 3, 'armor' => 0],
    ['cost' => 20, 'damage' => 0, 'armor' => 1],
    ['cost' => 40, 'damage' => 0, 'armor' => 2],
    ['cost' => 80, 'damage' => 0, 'armor' => 3]
];

class Character
{
    private $hit_points = 0;
    private $damage = 0;
    private $armor = 0;

    public function __construct(int $hit_points = 0, int $damage = 0, int $armor = 0)
    {
        $this->setHitPoints($hit_points);
        $this->setDamage($damage);
        $this->setArmor($armor);
    }

    public function setHitPoints(int $hit_points): void
    {
        $this->hit_points = $hit_points;
    }

    public function getHitPoints(): int
    {
        return $this->hit_points;
    }

    public function setDamage(int $damage): void
    {
        $this->damage = $damage;
    }

    public function getDamage(): int
    {
        return $this->damage;
    }

    public function setArmor(int $armor): void
    {
        $this->armor = $armor;
    }

    public function getArmor(): int
    {
        return $this->armor;
    }

    public function turnsNeededToDie(Character $opponent): int
    {
        return ceil($this->getHitPoints() / max($opponent->getDamage() - $this->getArmor(), 1));
    }

    public function wouldWinOf(Character $opponent)
    {
        return $opponent->turnsNeededToDie($this) <= $this->turnsNeededToDie($opponent);
    }
}

$player = new Character(100);
$boss   = new Character();

while (preg_match('/^([\w\s]+): (\d+)$/', fgets(STDIN), $stat)) {
    switch ($stat[1]) {
        case 'Hit Points':
            $boss->setHitPoints($stat[2]);
            break;
        case 'Damage':
            $boss->setDamage($stat[2]);
            break;
        case 'Armor':
            $boss->setArmor($stat[2]);
            break;
    }
}

$least_expensive_win = PHP_INT_MAX;
$most_expensive_loss = PHP_INT_MIN;

foreach (WEAPONS as $weapon) {
    foreach (ARMOR as $armor) {
        foreach (RINGS as $rl => $ring_left) {
            foreach (RINGS as $rr => $ring_right) {
                if ($rl === $rr) {
                    continue;
                }

                $player->setDamage($weapon['damage'] + $ring_left['damage'] + $ring_right['damage']);
                $player->setArmor($armor['armor'] + $ring_left['armor'] + $ring_right['armor']);
                $cost = $weapon['cost'] + $armor['cost'] + $ring_left['cost'] + $ring_right['cost'];

                if ($player->wouldWinOf($boss)) {
                    $least_expensive_win = min($least_expensive_win, $cost);
                } else {
                    $most_expensive_loss = max($most_expensive_loss, $cost);
                }
            }
        }
    }
}

fwrite(STDOUT, $least_expensive_win . PHP_EOL);
fwrite(STDOUT, $most_expensive_loss . PHP_EOL);