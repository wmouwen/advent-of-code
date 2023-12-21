<?php

$weights = new Ds\Vector;

while ($weight = intval(fgets(STDIN))) {
    $weights->push($weight);
}

function dividable(Ds\Vector $weights, int $groups): bool
{
    // TODO
    return true;
}

function combinationGenerator(Ds\Vector &$weights, int $remaining, Ds\Vector $used, Ds\Vector $result)
{
    if ($remaining <= 0) {
        yield $result;
        return;
    }

    for ($i = max($used->toArray() ?: [-1]) + 1; $i < count($weights); $i++) {
        $used->push($i);
        $result->push($weights[$i]);

        yield from combinationGenerator($weights, $remaining - 1, $used, $result);

        $result->pop();
        $used->pop();
    }
}

function untangle(Ds\Vector &$weights, int $nGroups): ?int
{
    // Optimisation: Sort weights from largest to smallest.
    $weights->sort(function (int $a, int $b): int {
        return $b <=> $a;
    });

    /** @var int $targetSum */
    $targetSum = intval($weights->sum() / $nGroups);

    // Pruning: Determine minimal group size for given weights needed to reach the $targetSum.
    $count = 0;
    for ($i = 0, $sum = 0; $sum < $targetSum && $count <= $weights->count(); $i++) {
        $sum += $weights->get($i);
        $count++;
    }

    /** @var int $bestProduct */
    $bestProduct = PHP_INT_MAX;

    for (; $bestProduct === PHP_INT_MAX && $count <= $weights->count(); $count++) {
        // Loop over all possible combinations for given $count.

        foreach (combinationGenerator($weights, $count, new Ds\Vector, new Ds\Vector) as $combination) {
            /** @var Ds\Vector $combination */

            if ($combination->sum() !== $targetSum) {
                continue;
            }

            /** @var int $product */
            $product = $combination->reduce(function (int $carry, int $value) {
                return $carry * $value;
            }, 1);
            if ($product >= $bestProduct) {
                continue;
            }

            /** @var Ds\Vector $remainder */
            $remainder = $weights->filter(function ($value) use ($combination) {
                return !$combination->contains($value);
            });
            if (!dividable($remainder, $nGroups - 1)) {
                continue;
            }

            // New best found!
            $bestProduct = $product;
        }
    }

    return $bestProduct;
}

fwrite(STDOUT, untangle($weights, 3) . PHP_EOL);
fwrite(STDOUT, untangle($weights, 4) . PHP_EOL);