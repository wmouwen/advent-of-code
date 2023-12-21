<?php

$vertices = $groups = [];

while ($row = str_replace(',', '', trim(fgets(STDIN)))) {
    $node = explode(' ', $row);
    for ($i = 2; $i < count($node); $i++) {
        $vertices[$vertices[$node[0]][] = $node[$i]][] = $node[0];
    }
}

for ($i = 0; ; $i++) {
    $todo = array_keys($vertices);
    foreach ($groups as $group) {
        $todo = array_diff($todo, $group ?? []);
    }

    if (empty($todo)) {
        break;
    }

    $todo = [reset($todo)];
    while (!empty($todo)) {
        if (!in_array($elm = array_pop($todo), $groups[$i] ?? [])) {
            $todo = array_unique(array_merge($todo, $vertices[$groups[$i][] = $elm]));
        }
    }
}

fwrite(STDOUT, count($groups[0]) . PHP_EOL);
fwrite(STDOUT, count($groups) . PHP_EOL);