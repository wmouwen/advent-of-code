<?php

class Node
{
    /** @var Node[] */
    public $children = [];

    /** @var int[] */
    public $metadata = [];

    public function __construct(&$input)
    {
        $nChildren = array_shift($input);
        $nMetadata = array_shift($input);

        for ($i = 0; $i < $nChildren; $i++) {
            $this->children[] = new Node($input);
        }

        for ($i = 0; $i < $nMetadata; $i++) {
            $this->metadata[] = array_shift($input);
        }
    }

    public function sumMetadataRecursively()
    {
        return array_reduce($this->children, function (int $carry, Node $child) {
            return $carry + $child->sumMetadataRecursively();
        }, array_sum($this->metadata));
    }

    public function sumSpecialRecursively()
    {
        if (empty($this->children)) {
            return array_sum($this->metadata);
        }

        $sum = 0;

        foreach ($this->metadata as $metadata) {
            if (isset($this->children[$metadata - 1])) {
                $sum += $this->children[$metadata - 1]->sumSpecialRecursively();
            }
        }

        return $sum;
    }
}

/** @var int[] $input */
$input = array_map('intval', explode(' ', trim(fgets(STDIN))));

$root = new Node($input);

fwrite(STDOUT, $root->sumMetadataRecursively() . PHP_EOL);
fwrite(STDOUT, $root->sumSpecialRecursively() . PHP_EOL);
