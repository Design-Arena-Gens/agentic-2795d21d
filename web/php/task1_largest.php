<?php
$numbers = [12, 45, 27];
$a = $numbers[0];
$b = $numbers[1];
$c = $numbers[2];
if ($a >= $b) {
    if ($a >= $c) {
        $largest = $a;
    } else {
        $largest = $c;
    }
} else {
    if ($b >= $c) {
        $largest = $b;
    } else {
        $largest = $c;
    }
}
echo "Input Numbers: " . implode(', ', $numbers) . "\n";
echo "Largest Number: $largest\n";
