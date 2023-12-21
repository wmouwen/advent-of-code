<?php

function intcodeProgram(array $memory): array
{
	/** @var int $ip Instruction Pointer */
	$ip = 0;

	while ($memory[$ip] !== 99) {
		switch ($memory[$ip]) {
			case 1:
				$memory[$memory[$ip + 3]] = $memory[$memory[$ip + 1]] + $memory[$memory[$ip + 2]];
				$ip += 4;
				break;

			case 2:
				$memory[$memory[$ip + 3]] = $memory[$memory[$ip + 1]] * $memory[$memory[$ip + 2]];
				$ip += 4;
				break;

			default:
				$ip++;
				break;
		}
	}

	return $memory;
}

$input = fgets(STDIN);
$memory = array_map('intval', explode(',', $input));

$memory[0x01] = 12;
$memory[0x02] = 2;
$output = intcodeProgram($memory);
fwrite(STDOUT, $output[0x00] . PHP_EOL);

for ($attempt = 0; $attempt < 10000; $attempt++) {
	$memory[0x01] = intval($attempt / 100);
	$memory[0x02] = $attempt % 100;

	$output = intcodeProgram($memory);

	if ($output[0x00] === 19690720) {
		fwrite(STDOUT, $attempt . PHP_EOL);
		break;
	}
}