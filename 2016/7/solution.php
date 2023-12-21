<?php

$tls_supported = 0;
$ssl_supported = 0;

while ($ip_address = trim(fgets(STDIN))) {
    if (!preg_match('/\[\w*?(\w)(\w)\2\1\w*?\]/', $ip_address)
        && preg_match('/(\w)(\w)\2\1/', preg_replace('/\[\w+\]/', '\[\]', $ip_address), $abba)
        && $abba[1] != $abba[2]) {
        $tls_supported++;
    }

    if (preg_match('/(\w)(\w)\1\w*?(\](\w*?\[\w*?\])*?|(\[\w*?\]\w*?)*?\[)\w*?\2\1\2/', $ip_address, $aba)
        && $aba[1] != $aba[2]) {
        $ssl_supported++;
    }
}

fwrite(STDOUT, $tls_supported . PHP_EOL);
fwrite(STDOUT, $ssl_supported . PHP_EOL);