<?php

// TODO: finish me

const ORDINAL_NUMBERS = [
    1 => 'first',
    2 => 'second',
    3 => 'third',
    4 => 'fouth'
];

class Microchip
{
    public $id;

    function __construct(string $id)
    {
        $this->id = $id;
    }
}

class RTG
{
    public $id;

    function __construct(string $id)
    {
        $this->id = $id;
    }
}

class TestingFacility
{
    private $backup = [[], [], [], []];
    public $floors = [[], [], [], []];

    public function backup()
    {
        $this->backup = $this->floors;
    }

    public function reset()
    {
        $this->floors = $this->backup;
    }
}

$facility = new TestingFacility();

while ($line = trim(fgets(STDIN))) {
    preg_match('/The (\w+) floor contains/', $line, $match);
    $floor = array_search($match[1], ORDINAL_NUMBERS) - 1;

    preg_match_all('/a (\w+)(-compatible)? (microchip|generator)/', $line, $matches, PREG_SET_ORDER);
    foreach ($matches as $match) {
        $facility->floors[$floor][] = $match[3] === 'microchip' ? new Microchip($match[1]) : new RTG($match[1]);
    }
}

