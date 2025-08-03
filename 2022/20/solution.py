import collections
import sys


def mix(encrypted: list[int], rounds: int) -> list[int]:
    decrypted = collections.deque(placeholder for placeholder in range(len(encrypted)))

    for _ in range(rounds):
        for placeholder, number in enumerate(encrypted):
            decrypted.rotate(-1 * decrypted.index(placeholder))
            decrypted.popleft()
            decrypted.rotate(-1 * number)
            decrypted.appendleft(placeholder)

    return list(encrypted[placeholder] for placeholder in decrypted)


def coordinates(decrypted: list[int]):
    return (
        decrypted[(decrypted.index(0) + offset) % len(decrypted)]
        for offset in (1000, 2000, 3000)
    )


def main():
    encrypted = [int(line.strip()) for line in sys.stdin]
    decrypted = mix(encrypted=encrypted, rounds=1)
    print(sum(coordinates(decrypted)))
    decrypted = mix(encrypted=[number * 811589153 for number in encrypted], rounds=10)
    print(sum(coordinates(decrypted)))


if __name__ == '__main__':
    main()
