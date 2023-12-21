<?php

class Wire
{
    private $inputs;
    private $logic;
    private $output;

    public function __construct(string $logic, string ...$inputs)
    {
        $this->logic  = $logic;
        $this->inputs = $inputs;
    }

    private function value(string $input)
    {
        if (preg_match('/^\d+$/', $input)) {
            return intval($input);
        }

        global $wires;

        return $wires[$input]->output();
    }

    private function calculateOutput(): void
    {
        switch ($this->logic) {
            case 'DIRECT':
                $this->output = $this->value($this->inputs[0]);
                break;
            case 'NOT':
                $this->output = ~$this->value($this->inputs[0]);
                break;
            case 'AND':
                $this->output = $this->value($this->inputs[0]) & $this->value($this->inputs[1]);
                break;
            case 'OR':
                $this->output = $this->value($this->inputs[0]) | $this->value($this->inputs[1]);
                break;
            case 'LSHIFT':
                $this->output = $this->value($this->inputs[0]) << $this->value($this->inputs[1]);
                break;
            case 'RSHIFT':
                $this->output = $this->value($this->inputs[0]) >> $this->value($this->inputs[1]);
                break;
        }

        $this->output &= 0xFFFF;
    }

    public function output(): ?int
    {
        if (is_null($this->output)) {
            $this->calculateOutput();
        }

        return $this->output;
    }

    public function reset(): void
    {
        $this->output = null;
    }
}

$wires = [];

while ($line = trim(fgets(STDIN))) {
    $explode = explode(' ', $line);
    switch (count($explode)) {
        case 3:
            $wires[$explode[2]] = new Wire('DIRECT', $explode[0]);
            break;
        case 4:
            $wires[$explode[3]] = new Wire($explode[0], $explode[1]);
            break;
        case 5:
            $wires[$explode[4]] = new Wire($explode[1], $explode[0], $explode[2]);
            break;
    }
}

fwrite(STDOUT, $a = $wires["a"]->output() . PHP_EOL);

foreach ($wires as $wire) {
    $wire->reset();
}
$wires["b"] = new Wire('DIRECT', $a);

fwrite(STDOUT, $wires["a"]->output() . PHP_EOL);