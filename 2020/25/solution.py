import sys


def transform(subject_number: int, loop_size: int):
    output = 1
    for _ in range(loop_size):
        output = (output * subject_number) % 20201227

    return output


def find_loop_size(public_key: int):
    output = 1
    loop_size = 1

    while True:
        output = (output * 7) % 20201227

        if output == public_key:
            return loop_size

        loop_size += 1


def main():
    print(
        transform(int(sys.stdin.readline()), find_loop_size(int(sys.stdin.readline())))
    )


if __name__ == '__main__':
    main()
