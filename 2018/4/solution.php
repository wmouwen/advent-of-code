<?php
/** @noinspection PhpUnhandledExceptionInspection */

/** @var string[] $input */
$input = [];

// Read input.
while ($row = trim(fgets(STDIN))) {
    $input[] = $row;
}
sort($input);

/** @var string[][] $guardIsActiveOnDays [guardId][] */
$guardIsActiveOnDays = [];

/** @var bool[][] $guardIsAsleepAtMinute [day][minute] */
$guardIsAsleepAtMinute = [];

// Compile the sleep-schedule.
foreach ($input as $row) {
    preg_match('/^\[(.*?)\]\s(wakes\sup|falls\sasleep|Guard\s#(\d+)\sbegins\sshift)$/', $row, $message);

    // Sometimes a guard starts just before midnight. Correct the datetime so he appears to start at midnight.
    $datetime = new DateTime($message[1]);
    if ($datetime->format('H') === '23') {
        $datetime
            ->add(new DateInterval('PT1H'))
            ->setTime(0, 0, 0);
    }

    $day = $datetime->format('m-d');

    switch ($message[2]) {
        case 'falls asleep':
            for ($minute = intval($datetime->format('i')); $minute < 60; $minute++) {
                $guardIsAsleepAtMinute[$day][$minute] = 1;
            }
            break;

        case 'wakes up':
            for ($minute = intval($datetime->format('i')); $minute < 60; $minute++) {
                $guardIsAsleepAtMinute[$day][$minute] = 0;
            }
            break;

        default:
            $guardId = $message[3];
            $guardIsActiveOnDays[$guardId][] = $day;
            $guardIsAsleepAtMinute[$day] = array_fill(0, 60, 0);
            break;
    }
}

function sleepiestMinute(array $days, array &$guardIsAsleepAtMinute): array
{
    $asleep = array_fill(0, 60, 0);

    foreach ($days as $day) {
        for ($i = 0; $i < count($asleep); $i++) {
            $asleep[$i] += $guardIsAsleepAtMinute[$day][$i];
        }
    }
    arsort($asleep);

    $minute = key($asleep);

    return [$minute, $asleep[$minute]];
}

/** @var int|null $sleepiestGuard */
$sleepiestGuard = null;

/** @var int $sleepiestMinutes */
$sleepiestMinutes = 0;

// Find the sleepiest guard.
foreach ($guardIsActiveOnDays as $guardId => $days) {
    $timeAsleep = array_reduce($days, function ($carry, $day) use ($guardIsAsleepAtMinute) {
        return $carry + array_sum($guardIsAsleepAtMinute[$day]);
    }, 0);

    if ($timeAsleep > $sleepiestMinutes) {
        $sleepiestGuard = $guardId;
        $sleepiestMinutes = $timeAsleep;
    }
}

[$minute,] = sleepiestMinute($guardIsActiveOnDays[$sleepiestGuard], $guardIsAsleepAtMinute);

fwrite(STDOUT, ($sleepiestGuard * $minute) . PHP_EOL);

/** @var int|null $sleepiestGuard */
$sleepiestGuard = null;
/** @var int $sleepiestMinutes */
$sleepiestMinutes = 0;
/** @var int|null $sleepiestMinute */
$sleepiestMinute = null;

// Find the sleepiest minute for any guard.
foreach ($guardIsActiveOnDays as $guardId => $days) {
    [$minute, $asleep] = sleepiestMinute($guardIsActiveOnDays[$guardId], $guardIsAsleepAtMinute);

    if ($asleep > $sleepiestMinutes) {
        $sleepiestGuard = $guardId;
        $sleepiestMinutes = $asleep;
        $sleepiestMinute = $minute;
    }
}

fwrite(STDOUT, ($sleepiestGuard * $sleepiestMinute) . PHP_EOL);
