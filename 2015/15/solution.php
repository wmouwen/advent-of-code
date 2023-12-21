<?php

class Ingredient
{
    public $capacity;
    public $durability;
    public $flavor;
    public $texture;
    public $calories;

    public function __construct(int $capacity, int $durability, int $flavor, int $texture, int $calories)
    {
        $this->capacity   = $capacity;
        $this->durability = $durability;
        $this->flavor     = $flavor;
        $this->texture    = $texture;
        $this->calories   = $calories;
    }
}

function best_recipe_score(array &$ingredients, int $diet = null, int $size = 100, int $depth = 0, array $amounts = [])
{
    switch ($depth - count($ingredients)) {
        case 0:
            if (array_sum($amounts) !== $size) {
                return PHP_INT_MIN;
            }
            $capacity = $durability = $flavor = $texture = $calories = 0;
            for ($i = 0; $i < count($ingredients); $i++) {
                $capacity   += $amounts[$i] * $ingredients[$i]->capacity;
                $durability += $amounts[$i] * $ingredients[$i]->durability;
                $flavor     += $amounts[$i] * $ingredients[$i]->flavor;
                $texture    += $amounts[$i] * $ingredients[$i]->texture;
                $calories   += $amounts[$i] * $ingredients[$i]->calories;
            }
            if (!is_null($diet) && $diet !== $calories) {
                return PHP_INT_MIN;
            }

            return max(0, $capacity) * max(0, $durability) * max(0, $flavor) * max(0, $texture);

        case 1:
            return best_recipe_score(
                $ingredients,
                $diet,
                $size,
                $depth + 1,
                array_merge($amounts, [$depth => $size - array_sum($amounts)])
            );

        default:
            $max = PHP_INT_MIN;
            for ($amount = 100 - array_sum($amounts); $amount >= 0; $amount--) {
                $max = max($max, best_recipe_score(
                    $ingredients,
                    $diet,
                    $size,
                    $depth + 1,
                    array_merge($amounts, [$depth => $amount])
                ));
            }

            return $max;
    }
}

$ingredients = [];
while (preg_match('/\w+: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)/', fgets(STDIN), $matches)) {
    $ingredients[] = new Ingredient($matches[1], $matches[2], $matches[3], $matches[4], $matches[5]);
}

fwrite(STDOUT, best_recipe_score($ingredients) . PHP_EOL);
fwrite(STDOUT, best_recipe_score($ingredients, 500) . PHP_EOL);