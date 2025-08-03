import sys

SNAFU_SYMBOLS = '=-012'
SNAFU_OFFSET = 2
SNAFU_BASE = len(SNAFU_SYMBOLS)


def snafu_to_dec(snafu: str) -> int:
    return sum(
        (SNAFU_SYMBOLS.index(value) - SNAFU_OFFSET)
        * (SNAFU_BASE ** (len(snafu) - index - 1))
        for index, value in enumerate(snafu)
    )


def dec_to_snafu(dec: int) -> str:
    snafu = []

    while dec:
        index = (dec + SNAFU_OFFSET) % len(SNAFU_SYMBOLS)
        snafu.insert(0, SNAFU_SYMBOLS[index])
        dec = (dec // SNAFU_BASE) + int(index < SNAFU_OFFSET)

    return ''.join(snafu)


def main():
    print(
        dec_to_snafu(
            sum(snafu_to_dec(snafu_number.strip()) for snafu_number in sys.stdin)
        )
    )


if __name__ == '__main__':
    main()
