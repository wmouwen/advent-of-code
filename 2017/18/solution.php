<?php

class Program
{
    private $registers = [];
    private $instructions = [];

    private $pc = 0;

    private $terminated = false;
    private $awaiting_input = false;

    private $input = [];
    private $output = [];

    private $send_count = 0;

    public function __construct(int $pid, array $instructions)
    {
        $this->instructions   = $instructions;
        $this->registers      = array_fill_keys(range('a', 'z'), 0);
        $this->registers["p"] = $pid;
    }

    private function val(string $arg): int
    {
        return is_numeric($arg) ? intval($arg) : $this->registers[$arg];
    }

    public function runUntilBlocked(): void
    {
        if ($this->terminated || $this->awaiting_input) {
            return;
        }

        while (0 <= $this->pc && $this->pc < count($this->instructions)) {
            $instr = $this->instructions[$this->pc];
            switch ($instr[0]) {
                case 'set':
                    $this->registers[$instr[1]] = $this->val($instr[2]);
                    break;

                case 'add':
                    $this->registers[$instr[1]] += $this->val($instr[2]);
                    break;

                case 'mul':
                    $this->registers[$instr[1]] *= $this->val($instr[2]);
                    break;

                case 'mod':
                    $this->registers[$instr[1]] %= $this->val($instr[2]);
                    break;

                case 'jgz':
                    if ($this->val($instr[1]) > 0) {
                        $this->pc += $this->val($instr[2]) - 1;
                    }
                    break;

                case 'rcv':
                    if (empty($this->input)) {
                        $this->awaiting_input = true;

                        return;
                    }
                    $this->registers[$instr[1]] = array_shift($this->input);
                    break;

                case 'snd':
                    array_push($this->output, $this->val($instr[1]));
                    $this->send_count++;
                    break;
            }
            $this->pc++;
        }
        $this->terminated = true;
    }

    public function getOutput(): ?int
    {
        return array_shift($this->output);
    }

    public function input(int $value): void
    {
        array_push($this->input, $value);
        $this->awaiting_input = false;
    }

    public function isAwaitingInput(): bool
    {
        return $this->awaiting_input;
    }

    public function isTerminated(): bool
    {
        return $this->terminated;
    }

    public function getSendCount(): int
    {
        return $this->send_count;
    }
}

$instructions = [];
while ($instruction = trim(fgets(STDIN))) {
    $instructions[] = explode(' ', $instruction);
}

$programs = [
    new Program(0, $instructions),
    new Program(1, $instructions)
];

$part_one = null;

for ($i = 0; !$programs[0]->isTerminated() || !$programs[1]->isTerminated(); $i = !$i) {
    if ($programs[$i]->isTerminated()) {
        continue;
    }
    if ($programs[$i]->isAwaitingInput() && ($programs[!$i]->isAwaitingInput() || $programs[!$i]->isTerminated())) {
        break;
    }

    $programs[$i]->runUntilBlocked();
    while ($output = $programs[$i]->getOutput()) {
        $programs[!$i]->input($output);
        $tmp = $output ?? $tmp ?? null;
    }
    $part_one = $part_one ?? $tmp;
}

fwrite(STDOUT, $part_one . PHP_EOL);
fwrite(STDOUT, $programs[1]->getSendCount() . PHP_EOL);