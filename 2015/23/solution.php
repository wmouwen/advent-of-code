<?php

class TuringLock
{
    private $reg = [];
    private $instructions = [];
    private $pc = 0;

    public function __construct(array $instructions)
    {
        $this->reg          = array_fill_keys(range('a', 'b'), 0);
        $this->instructions = $instructions;
    }

    private function val(string $arg): int
    {
        return is_numeric($arg) ? intval($arg) : $this->reg[$arg];
    }

    public function run(): void
    {
        while (0 <= $this->pc && $this->pc < count($this->instructions)) {
            $instr = $this->instructions[$this->pc];

            switch ($instr[0]) {
                case 'hlf':
                    $this->reg[$instr[1]] = $this->val($instr[1]) >> 1;
                    break;

                case 'tpl':
                    $this->reg[$instr[1]] = $this->val($instr[1]) * 3;
                    break;

                case 'inc':
                    $this->reg[$instr[1]]++;
                    break;

                case 'jmp':
                    $this->pc += $this->val($instr[1]) - 1;
                    break;

                case 'jie':
                    if (($this->val($instr[1]) & 1) === 0) {
                        $this->pc += $this->val($instr[2]) - 1;
                    }
                    break;

                case 'jio':
                    if ($this->val($instr[1]) === 1) {
                        $this->pc += $this->val($instr[2]) - 1;
                    }
                    break;
            }

            $this->pc++;
        }
    }

    public function getRegisterValue(string $register): ?int
    {
        return $this->reg[$register] ?? null;
    }

    public function setRegisterValue(string $register, int $value): void
    {
        $this->reg[$register] = $value;
    }
}

$instructions = [];
while ($line = fgets(STDIN)) {
    $instructions[] = explode(' ', str_replace(',', '', trim($line)));
}

$program = new TuringLock($instructions);
$program->run();
fwrite(STDOUT, $program->getRegisterValue('b') . PHP_EOL);

$program = new TuringLock($instructions);
$program->setRegisterValue('a', 1);
$program->run();
fwrite(STDOUT, $program->getRegisterValue('b') . PHP_EOL);