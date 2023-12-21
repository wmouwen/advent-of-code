<?php

class Monorail
{
    private $registers = [];
    private $instructions = [];
    private $program_counter = 0;

    public function __construct(array $instructions)
    {
        $this->instructions = $instructions;
    }

    private function val(string $argument): int
    {
        return is_numeric($argument) ? intval($argument) : ($this->registers[$argument] ?? 0);
    }

    public function run(): void
    {
        while (0 <= $this->program_counter && $this->program_counter < count($this->instructions)) {
            $instruction = $this->instructions[$this->program_counter];

            switch ($instruction[0]) {
                case 'cpy':
                    $this->registers[$instruction[2]] = $this->val($instruction[1]);
                    break;

                case 'inc':
                    $this->registers[$instruction[1]]++;
                    break;

                case 'dec':
                    $this->registers[$instruction[1]]--;
                    break;

                case 'jnz':
                    if ($this->val($instruction[1]) !== 0) {
                        $this->program_counter += $this->val($instruction[2]) - 1;
                    }
                    break;
            }

            $this->program_counter++;
        }
    }

    public function getRegisterValue(string $register): ?int
    {
        return $this->registers[$register] ?? null;
    }

    public function setRegisterValue(string $register, int $value): void
    {
        $this->registers[$register] = $value;
    }
}

$instructions = [];
while ($line = trim(fgets(STDIN))) {
    $instructions[] = explode(' ', $line);
}

$program = new Monorail($instructions);
$program->run();
fwrite(STDOUT, $program->getRegisterValue('a') . PHP_EOL);

$program = new Monorail($instructions);
$program->setRegisterValue('c', 1);
$program->run();
fwrite(STDOUT, $program->getRegisterValue('a') . PHP_EOL);