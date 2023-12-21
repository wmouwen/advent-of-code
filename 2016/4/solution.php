<?php

$sum_room_ids   = 0;
$object_storage = null;

while (preg_match('/^([\w\-]+)-(\d+)\[([\w]{5})\]$/', trim(fgets(STDIN)), $room)) {
    list(, $name, $id, $checksum) = $room;

    $letter_occurrences = array_count_values(str_split(str_replace('-', '', $name)));
    $letters            = array_keys($letter_occurrences);
    $occurrences        = array_values($letter_occurrences);

    array_multisort($occurrences, SORT_DESC, $letters, SORT_ASC, $letter_occurrences);

    if (implode(array_splice($letters, 0, 5)) === $checksum) {
        $sum_room_ids += $id;

        for ($i = 0; $i < strlen($name); $i++) {
            $name[$i] = $name[$i] == '-' ? ' ' : chr(97 + ((ord($name[$i]) - 97 + $id) % 26));
        }

        if ($name === 'northpole object storage') {
            $object_storage = $id;
        }
    }
}

fwrite(STDOUT, $sum_room_ids . PHP_EOL);
fwrite(STDOUT, $object_storage . PHP_EOL);
