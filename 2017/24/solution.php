<?php

class Component
{
    private $used = false;
    private $ports = [];

    public function __construct(array $ports)
    {
        $this->ports = $ports;
    }

    public function strength(): ?int
    {
        return $this->ports[0] + $this->ports[1];
    }

    public function isUsed(): bool
    {
        return $this->used;
    }

    public function use()
    {
        $this->used = true;
    }

    public function free()
    {
        $this->used = false;
    }

    public function getOtherPort(int $value): ?int
    {
        if ($value === $this->ports[0]) {
            return $this->ports[1];
        }
        if ($value === $this->ports[1]) {
            return $this->ports[0];
        }

        return null;
    }
}

$component_groups = [];
while ($line = fgets(STDIN)) {
    $ports     = array_map('intval', explode('/', trim($line)));
    $component = new Component($ports);

    $component_groups[$ports[0]][] = $component;
    $component_groups[$ports[1]][] = $component;
}

function findStrongestBridge(int $port, array &$component_groups): int
{
    $strength = 0;

    foreach ($component_groups[$port] as $component) {
        if ($component->isUsed()) {
            continue;
        }

        $component->use();

        $strength = max(
            $strength,
            $component->strength() + findStrongestBridge($component->getOtherPort($port), $component_groups)
        );

        $component->free();
    }

    return $strength;
}

fwrite(STDOUT, findStrongestBridge(0, $component_groups) . PHP_EOL);

function findLongestBridge(int $port, array &$component_groups): array
{
    $length   = 0;
    $strength = 0;

    foreach ($component_groups[$port] as $component) {
        if ($component->isUsed()) {
            continue;
        }

        $component->use();

        $ret = findLongestBridge($component->getOtherPort($port), $component_groups);
        $ret[0]++;
        $ret[1] += $component->strength();

        if ($ret[0] > $length) {
            $length   = $ret[0];
            $strength = $ret[1];
        } elseif ($ret[0] == $length) {
            $strength = max($strength, $ret[1]);
        }

        $component->free();
    }

    return [$length, $strength];
}

fwrite(STDOUT, findLongestBridge(0, $component_groups)[1] . PHP_EOL);