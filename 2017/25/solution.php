<?php

class Machine
{
    private $tape = [];
    private $cursor = 0;

    private $states = [];
    private $token = 'A';

    public function __construct(string $token)
    {
        $this->token = $token;
    }

    public function addState(State $state): void
    {
        $this->states[$state->getID()] = $state;
    }

    public function run(int $steps = 1): void
    {
        while ($steps--) {
            $state       = $this->states[$this->token];
            $instruction = $state->getInstruction($this->tape[$this->cursor] ?? 0);

            $this->tape[$this->cursor] = $instruction->getWrite();
            $this->cursor              = $instruction->getMove() + $this->cursor;
            $this->token               = $instruction->getNext();
        }
    }

    public function getChecksum(): int
    {
        return array_count_values($this->tape)[1] ?? 0;
    }
}

class State
{
    private $id;
    private $instructions = [];

    public function __construct(string $id)
    {
        $this->id = $id;
    }

    public function getID()
    {
        return $this->id;
    }

    public function addInstruction(int $for, Instruction $instruction): void
    {
        $this->instructions[$for] = $instruction;
    }

    public function getInstruction(int $for): Instruction
    {
        return $this->instructions[$for];
    }
}

class Instruction
{
    private $write = 1;
    private $move = 1;
    private $next = 'A';

    public function __construct(int $write, int $move, string $next)
    {
        $this->write = $write;
        $this->move  = $move;
        $this->next  = $next;
    }

    public function getWrite(): int
    {
        return $this->write;
    }

    public function getMove(): int
    {
        return $this->move;
    }

    public function getNext(): string
    {
        return $this->next;
    }
}

preg_match('/Begin in state (\w)./', fgets(STDIN), $match);
$machine = new Machine($match[1]);

preg_match('/Perform a diagnostic checksum after (\d+) steps./', fgets(STDIN), $match);
$steps = $match[1];

while ($line = fgets(STDIN)) {
    if (preg_match('/In state (\w):/', $line, $match)) {
        $state = new State($match[1]);

        while (preg_match('/If the current value is (\d):/', fgets(STDIN), $match_for)) {
            preg_match('/Write the value (\d)./', fgets(STDIN), $match_write);
            preg_match('/Move one slot to the (\w+)./', fgets(STDIN), $match_move);
            preg_match('/Continue with state (\w)./', fgets(STDIN), $match_next);

            $instruction = new Instruction(intval($match_write[1]), $match_move[1] == 'left' ? -1 : 1, $match_next[1]);
            $state->addInstruction(intval($match_for[1]), $instruction);
        }

        $machine->addState($state);
    }
}

$machine->run($steps);

fwrite(STDOUT, $machine->getChecksum() . PHP_EOL);