import sys

Dish = list[list[str]]


def tilt(dish: Dish) -> Dish:
    for x in range(len(dish[0])):
        slide_to = 0

        for y in range(len(dish)):
            if dish[y][x] == '#' or (dish[y][x] == 'O' and slide_to == y):
                slide_to = y + 1
            elif dish[y][x] == 'O':
                dish[slide_to][x] = 'O'
                dish[y][x] = '.'
                slide_to += 1

    return dish


def spin(dish: Dish) -> Dish:
    return list(map(list, zip(*reversed(dish))))


def cycle(dish: Dish) -> Dish:
    for i in range(4):
        dish = spin(tilt(dish))

    return dish


def state(dish: Dish) -> str:
    return '\n'.join(map(lambda row: ''.join(row), dish))


def find_final_dish(dish: Dish, cycles: int) -> Dish:
    states = [state(dish)]

    for i in range(cycles):
        dish = cycle(dish)

        current_state = state(dish)
        if current_state in states:
            loop_start = states.index(current_state)
            loop_restart = i + 1
            loop_remainder = (cycles - loop_restart) % (loop_restart - loop_start)
            final_dish = states[loop_start + loop_remainder]
            return [list(line) for line in final_dish.split('\n')]

        states.append(current_state)

    return dish


def load(dish: Dish) -> int:
    return sum(len(dish) - y for y, row in enumerate(dish) for cell in row if cell == 'O')


dish: Dish = [line for line in map(lambda line: list(line.strip()), sys.stdin)]

dish = tilt(dish)
print(load(dish))

dish = find_final_dish(dish, 1000000000)
print(load(dish))
