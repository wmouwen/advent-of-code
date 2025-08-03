import re
import sys

valid_part_one = 0
valid_part_two = 0

for line in sys.stdin:
    output = re.match(r'(\d+)-(\d+) (\w): (\w+)', line)
    a, b = int(output.group(1)), int(output.group(2))
    char, password = output.group(3, 4)

    valid_part_one += a <= password.count(char) <= b
    valid_part_two += (password[a - 1] == char or password[b - 1] == char) and password[
        a - 1
    ] != password[b - 1]

print(valid_part_one)
print(valid_part_two)
