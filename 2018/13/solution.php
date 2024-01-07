<?php

declare(strict_types=1);
assert(PHP_VERSION_ID >= 80214);

class Cart
{
    public int $x;
    public int $y;
    public int $vx;
    public int $vy;

    public int $t = -1;
    public bool $dead = false;

    public function __construct(int $y, int $x, string $char)
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

    public function move(): void
    {
        $this->y += $this->vy;
        $this->x += $this->vx;
    }

    public function interact($char): void
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

    protected function turn(): void
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

/** @var list<list<string>> $map */
$map = [];
while ($input = trim(fgets(STDIN), "\t\n\r\0\x0B")) {
    $map[] = str_split($input);
}

/** @var list<Cart> $carts */
$carts = [];

/** @var list<string> $locations */
$locations = [];

for ($y = 0; $y < count($map); $y++) {
    for ($x = 0; $x < count($map[$y]); $x++) {
        if (in_array($map[$y][$x], ['^', '>', 'v', '<'])) {
            $carts[] = (new Cart($y, $x, $map[$y][$x]));
            $locations[] = implode(',', [$y, $x]);

            $map[$y][$x] = in_array($map[$y][$x], ['>', '<']) ? '-' : '|';
        }
    }
}

$hadFirstContact = false;

for ($tick = 0; count($carts) > 1; $tick++) {
    usort($carts, function ($a, $b) {
        return ($a->y <=> $b->y) ?: ($a->x <=> $b->x);
    });

    foreach ($carts as $cart) {
        if ($cart->dead) {
            continue;
        }

        $locations = array_diff($locations, [implode(',', [$cart->y, $cart->x])]);
        $cart->move();

        if (in_array(implode(',', [$cart->y, $cart->x]), $locations)) {
            $locations = array_diff($locations, [implode(',', [$cart->y, $cart->x])]);

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
        $locations[] = implode(',', [$cart->y, $cart->x]);
    }

    $newCarts = [];
    foreach ($carts as $cart) {
        if (!$cart->dead) {
            $newCarts[] = ($cart);
        }
    }
    $carts = $newCarts;
}

$last = reset($carts);

fwrite(STDOUT, sprintf('%d,%d', $last->x, $last->y) . PHP_EOL);
