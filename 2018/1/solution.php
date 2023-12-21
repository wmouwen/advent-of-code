<?php

/** @var int $frequency The current frequency. */
$frequency = 0;

/** @var bool[] $changes Input cache. */
$changes = [];

/** @var int|null $firstRevisit The first frequency to be revisited. */
$firstRevisit = null;

/** @var Ds\Set $visited List of visited frequencies. */
$visited = new Ds\Set;

/** @var string $row */
while ($row = trim(fgets(STDIN))) {

    /** @var int $change */
    $change = intval($row);

    // Store change for re-use if needed.
    $changes[] = $change;

    // Apply change.
    $frequency += $change;

    // Detect revisits.
    if ($visited->contains($frequency)) {
        $firstRevisit = $firstRevisit ?? $frequency;
    } else {
        $visited->add($frequency);
    }
}

fwrite(STDOUT, $frequency . PHP_EOL);

// Continue searching for a revisit if one loop was not enough.
while ($firstRevisit === null) {
    foreach ($changes as $change) {
        // Apply change.
        $frequency += $change;

        // Detect revisits. Break on the first revisit.
        if ($visited->contains($frequency)) {
            $firstRevisit = $frequency;
            break;
        }

        $visited->add($frequency);
    }
}

fwrite(STDOUT, $firstRevisit . PHP_EOL);
