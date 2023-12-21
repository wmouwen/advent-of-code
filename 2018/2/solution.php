<?php

/** @var int $duplicates Amount of boxes with duplicate letters. */
$duplicates = 0;

/** @var int $triplicates Amount of boxes with triplicate letters. */
$triplicates = 0;

/** @var string[] $boxes List of box ID's. */
$boxes = [];

/** @var string|null $similarity */
$similarity = null;

/**
 * @param string $a
 * @param string $b String which differs by a single character with $a.
 * @return string|null
 */
function extract_similarity(string $a, string $b): ?string
{
    for ($i = 0; $i < strlen($a); $i++) {
        if ($a[$i] !== $b[$i]) {
            return substr($a, 0, $i) . substr($a, $i + 1);
        }
    }

    return null;
}

/** @var string $box */
while ($box = trim(fgets(STDIN))) {

    // Search for duplicates and triplicates.
    $counts = array_count_values(str_split($box));
    if (in_array(2, $counts)) {
        $duplicates++;
    }
    if (in_array(3, $counts)) {
        $triplicates++;
    }

    if ($similarity === null) {
        // Search for a similarity between the current box and all previous.
        foreach ($boxes as $other) {
            if (levenshtein($box, $other) === 1) {
                $similarity = extract_similarity($box, $other);
                break;
            }
        }

        $boxes[] = $box;
    }
}

fwrite(STDOUT, ($duplicates * $triplicates) . PHP_EOL);
fwrite(STDOUT, $similarity . PHP_EOL);
