<?php

class Requirement
{
    public $parents = [];
    public $children = [];
    public $finishes = 0;
}

$requirements = [];

while (preg_match('/^Step (\w) must be finished before step (\w) can begin\.$/', trim(fgets(STDIN)), $input)) {
    $parent = $requirements[$input[1]] = ($requirements[$input[1]] ?? new Requirement);
    $child = $requirements[$input[2]] = ($requirements[$input[2]] ?? new Requirement);
    $parent->children[] = $input[2];
    $child->parents[] = $input[1];
}

$roots = [];

foreach ($requirements as $id => $requirement) {
    if (empty($requirement->parents)) {
        $roots[] = $id;
    }
}

$todo = $roots;

$sequence = [];

do {
    sort($todo);
    $node = array_shift($todo);

    $sequence[] = $node;

    foreach ($requirements[$node]->children as $child) {
        $available = array_reduce($requirements[$child]->parents, function ($carry, $parent) use (&$sequence) {
            return $carry && in_array($parent, $sequence);
        }, true);
        if ($available) {
            $todo[] = $child;
        }
    }

} while (!empty($todo));

fwrite(STDOUT, implode($sequence) . PHP_EOL);

$todo = $roots;
sort($todo);

$sequence = [];

$worker = [];
$time = 0;

while (!empty($worker) || !empty($todo)) {
    for ($i = 0; $i < 5; $i++) {
        if (isset($worker[$i]) && $requirements[$worker[$i]]->finishes <= $time) {
            $sequence[] = $worker[$i];
            foreach ($requirements[$worker[$i]]->children as $child) {
                $available = array_reduce($requirements[$child]->parents, function ($carry, $parent) use (&$sequence) {
                    return $carry && in_array($parent, $sequence);
                }, true);
                if ($available) {
                    $todo[] = $child;
                }
            }
            unset($worker[$i]);
        }
    }

    sort($todo);

    for ($i = 0; $i < 5; $i++) {
        if (!isset($worker[$i]) && !empty($todo)) {
            $worker[$i] = array_shift($todo);
            $requirements[$worker[$i]]->finishes = $time + ord($worker[$i]) - ord('A') + 61;
        }
    }

    $time++;
}

fwrite(STDOUT, ($time - 1) . PHP_EOL);
