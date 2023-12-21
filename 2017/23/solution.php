<?php

class CompositeNumbersCounter
{
    private $reg = [];
    private $instructions = [];

    private $pc = 0;

    private $original_input = null;
    private $instr_counts = [];

    public function __construct(array $instructions)
    {
        $this->reg            = array_fill_keys(range('a', 'h'), 0);
        $this->instructions   = $instructions;
        $this->original_input = intval($instructions[0][2]);
    }

    private function val(string $arg): int
    {
        return is_numeric($arg) ? intval($arg) : $this->reg[$arg];
    }

    public function runOriginal(): void
    {
        while (0 <= $this->pc && $this->pc < count($this->instructions)) {
            $instr = $this->instructions[$this->pc];
            switch ($instr[0]) {
                case 'set':
                    $this->reg[$instr[1]] = $this->val($instr[2]);
                    break;

                case 'sub':
                    $this->reg[$instr[1]] -= $this->val($instr[2]);
                    break;

                case 'mul':
                    $this->reg[$instr[1]] *= $this->val($instr[2]);
                    break;

                case 'jnz':
                    if ($this->val($instr[1]) !== 0) {
                        $this->pc += $this->val($instr[2]) - 1;
                    }
                    break;
            }

            $this->instr_counts[$instr[0]] = ($this->instr_counts[$instr[0]] ?? 0) + 1;
            $this->pc++;
        }
    }

    public function runOptimized(): int
    {
        $this->reg['b'] = $this->reg['c'] = $this->original_input;

        if ($this->reg['a']) {
            $this->reg['b'] = $this->reg['b'] * 100 + 100000;
            $this->reg['c'] = $this->reg['b'] + 17000;
        }

        while (true) {
            $this->reg['f'] = 1;

            for ($this->reg['d'] = 2; $this->reg['d'] !== $this->reg['b']; $this->reg['d']++) {
                for ($this->reg['e'] = intval($this->reg['b'] / $this->reg['d']); ($this->reg['d'] * $this->reg['e']) <= $this->reg['b']; $this->reg['e']++) {
                    if ($this->reg['d'] * $this->reg['e'] === $this->reg['b']) {
                        $this->reg['f'] = 0;
                        break 2;
                    }
                }
            }

            if (!$this->reg['f']) {
                $this->reg['h']++;
            }

            if ($this->reg['b'] >= $this->reg['c']) {
                break;
            }

            $this->reg['b'] += 17;
        }

        return $this->reg['h'];
    }

    public function getInstructionCount(string $instr): ?int
    {
        return $this->instr_counts[$instr] ?? null;
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

while ($line = fgets(STDIN)) {
    $instructions[] = explode(' ', trim($line));
}

$program = new CompositeNumbersCounter($instructions);
$program->runOriginal();
fwrite(STDOUT, $program->getInstructionCount('mul') . PHP_EOL);

$program = new CompositeNumbersCounter($instructions);
$program->setRegisterValue('a', 1);
fwrite(STDOUT, $program->runOptimized() . PHP_EOL);