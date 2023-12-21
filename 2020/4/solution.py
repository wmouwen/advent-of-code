import re
import sys


class Passport:
    def __init__(self):
        self.data = {
            # (Birth Year)
            'byr': None,
            # (Issue Year)
            'iyr': None,
            # (Expiration Year)
            'eyr': None,
            # (Height)
            'hgt': None,
            # (Hair Color)
            'hcl': None,
            # (Eye Color)
            'ecl': None,
            # (Passport ID)
            'pid': None,
            # (Country ID)
            'cid': None
        }

    def __setitem__(self, key: str, value: str):
        self.data[key] = value

    def __getattr__(self, item: str):
        return self.data[item]

    def all_fields_present(self) -> bool:
        return self.byr is not None \
               and self.iyr is not None \
               and self.eyr is not None \
               and self.hgt is not None \
               and self.hcl is not None \
               and self.ecl is not None \
               and self.pid is not None

    def all_fields_valid(self) -> bool:
        if not self.all_fields_present():
            return False

        hgt = re.match(r'(\d+)(\w+)', self.hgt)
        hgt_amount = int(hgt.group(1))
        hgt_unit = str(hgt.group(2))

        return 1920 <= int(self.byr) <= 2002 \
               and 2010 <= int(self.iyr) <= 2020 \
               and 2020 <= int(self.eyr) <= 2030 \
               and ((hgt_unit == 'cm' and 150 <= hgt_amount <= 193) or (hgt_unit == 'in' and 59 <= hgt_amount <= 76)) \
               and bool(re.search(r'^#[0-9a-z]{6}$', self.hcl)) \
               and self.ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'] \
               and bool(re.search(r'^\d{9}$', self.pid))


passports = [Passport()]

for line in sys.stdin:
    line = line.strip()

    if not line.strip():
        passports.append(Passport())
        continue

    for field in line.strip().split():
        key, value = field.split(':')
        passports[-1][key] = value

valid_passports = list(filter(lambda passport: passport.all_fields_present(), passports))
print(len(valid_passports))
print(sum(passport.all_fields_valid() for passport in valid_passports))
