<?php

const REACTING_UNITS = [
    'aA', 'Aa', 'bB', 'Bb', 'cC', 'Cc', 'dD', 'Dd', 'eE', 'Ee', 'fF', 'Ff', 'gG', 'Gg',
    'hH', 'Hh', 'iI', 'Ii', 'jJ', 'Jj', 'kK', 'Kk', 'lL', 'Ll', 'mM', 'Mm', 'nN', 'Nn',
    'oO', 'Oo', 'pP', 'Pp', 'qQ', 'Qq', 'rR', 'Rr', 'sS', 'Ss', 'tT', 'Tt', 'uU', 'Uu',
    'vV', 'Vv', 'wW', 'Ww', 'xX', 'Xx', 'yY', 'Yy', 'zZ', 'Zz',
];

function reduce(string $polymer): string
{
    do {
        $polymer = str_replace(REACTING_UNITS, '', $polymer, $count);
    } while ($count > 0);

    return $polymer;
}

$reduced = reduce(trim(fgets(STDIN)));

fwrite(STDOUT, strlen($reduced) . PHP_EOL);

/** @var int $shortest */
$shortest = PHP_INT_MAX;

foreach (range('a', 'z') as $troublemaker) {
    $filtered = reduce(str_replace([$troublemaker, strtoupper($troublemaker)], '', $reduced));
    $shortest = min($shortest, strlen($filtered));
}

fwrite(STDOUT, $shortest . PHP_EOL);
