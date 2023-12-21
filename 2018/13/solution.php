<?php

class Cart
{
    public $x;
    public $y;

    public $vx;
    public $vy;

    public $t = -1;
    public $dead = false;

    public function __construct($y, $x, $char)
    {
        $this->y = $y;
        $this->x = $x;

        switch ($char) {
            case '^':
                $this->vy = -1;
                $this->vx = 0;
                break;

            case '>':
                $this->vy = 0;
                $this->vx = 1;
                break;

            case 'v':
                $this->vy = 1;
                $this->vx = 0;
                break;

            case '<':
                $this->vy = 0;
                $this->vx = -1;
                break;
        }
    }

    public function move()
    {
        $this->y += $this->vy;
        $this->x += $this->vx;
    }

    public function interact($char)
    {
        switch ($char) {
            case '-';
            case '|';
                break;

            case '\\';
                $vy = $this->vy;
                $vx = $this->vx;
                $this->vy = $vx;
                $this->vx = $vy;
                break;

            case '/';
                $vy = $this->vy;
                $vx = $this->vx;
                $this->vy = -$vx;
                $this->vx = -$vy;
                break;

            case '+';
                $this->turn();
                break;

            case ' ':
            default:
                throw new RuntimeException;
        }
    }

    protected function turn()
    {
        switch ($this->t) {
            case -1:
                $vy = $this->vy;
                $vx = $this->vx;
                $this->vy = -$vx;
                $this->vx = $vy;
                break;

            case 1:
                $vy = $this->vy;
                $vx = $this->vx;
                $this->vy = $vx;
                $this->vx = -$vy;
                break;
        }

        $this->t = (($this->t + 2) % 3) - 1;
    }
}

$map = [];
while ($input = trim(fgets(STDIN), "\t\n\r\0\x0B")) {
    $map[] = str_split($input);
}

/** @var \Ds\Set|Cart[] $carts */
$carts = new \Ds\Set;
$locations = new \Ds\Set;

for ($y = 0; $y < count($map); $y++) {
    for ($x = 0; $x < count($map[$y]); $x++) {
        if (in_array($map[$y][$x], ['^', '>', 'v', '<'])) {
            $carts->add(new Cart($y, $x, $map[$y][$x]));
            $locations->add([$y, $x]);

            $map[$y][$x] = in_array($map[$y][$x], ['>', '<']) ? '-' : '|';
        }
    }
}

$hadFirstContact = false;

for ($tick = 0; $carts->count() > 1; $tick++) {
    $carts->sort(function ($a, $b) {
        return ($a->y <=> $b->y) ?: ($a->x <=> $b->x);
    });

    foreach ($carts as $cart) {
        if ($cart->dead) {
            continue;
        }

        $locations->remove([$cart->y, $cart->x]);
        $cart->move();

        if ($locations->contains([$cart->y, $cart->x])) {
            $locations->remove([$cart->y, $cart->x]);

            $cart->dead = true;
            foreach ($carts as $other) {
                if ($cart !== $other && $cart->x === $other->x && $cart->y === $other->y) {
                    $other->dead = true;
                    break;
                }
            }

            if (!$hadFirstContact) {
                fwrite(STDOUT, sprintf('%d,%d', $cart->x, $cart->y) . PHP_EOL);
                $hadFirstContact = true;
            }

            continue;
        }

        $cart->interact($map[$cart->y][$cart->x]);
        $locations->add([$cart->y, $cart->x]);
    }

    $newCarts = new \Ds\Set;
    foreach ($carts as $cart) {
        if (!$cart->dead) {
            $newCarts->add($cart);
        }
    }
    $carts = $newCarts;
}

$last = $carts->first();

fwrite(STDOUT, sprintf('%d,%d', $last->x, $last->y) . PHP_EOL);
