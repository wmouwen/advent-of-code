<?php

class Bot
{
    public $low = null;
    public $high = null;
    public $inputs = [];

    public function resolveOutputs()
    {
        for ($i = 0; $i < count($this->inputs); $i++) {
            if (is_array($this->inputs[$i])) {
                $this->inputs[$i] = $this->inputs[$i][0]->getOutput($this->inputs[$i][1]);
            }
        }

        $this->low  = min($this->inputs);
        $this->high = max($this->inputs);
    }

    public function getOutput(string $output): int
    {
        if (is_null($this->low)) {
            $this->resolveOutputs();
        }

        return $output === 'low' ? $this->low : $this->high;
    }
}

$bots    = [];
$outputs = [];

while ($line = trim(fgets(STDIN))) {
    $instruction = explode(' ', $line);

    if ($instruction[0] === 'value') {
        list(, $value, , , , $bot_id) = $instruction;
        $bot           = ($bots[$bot_id] = $bots[$bot_id] ?? new Bot());
        $bot->inputs[] = intval($value);

    } else {
        list(, $bot_id, , , , $low_type, $low_id, , , , $high_type, $high_id) = $instruction;
        $bot = ($bots[$bot_id] = $bots[$bot_id] ?? new Bot());

        if ($low_type === 'output') {
            $outputs[$low_id] = &$bot->low;
        } else {
            $bots[$low_id]           = $bots[$low_id] ?? new Bot();
            $bots[$low_id]->inputs[] = [$bot, 'low'];
        }

        if ($high_type === 'output') {
            $outputs[$high_id] = &$bot->high;
        } else {
            $bots[$high_id]           = $bots[$high_id] ?? new Bot();
            $bots[$high_id]->inputs[] = [$bot, 'high'];
        }
    }
}

foreach ($bots as $id => $bot) {
    $bot->resolveOutputs();
    if ($bot->low === 17 && $bot->high === 61) {
        fwrite(STDOUT, $id . PHP_EOL);
    }
}

ksort($outputs);
fwrite(STDOUT, array_product(array_splice($outputs, 0, 3)) . PHP_EOL);