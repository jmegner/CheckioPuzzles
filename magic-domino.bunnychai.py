import itertools
import random


DOMINO = [(i, j) for i in range(7) for j in range(7) if j >= i]


# all cols that sum up to number
def all_cols(size, number):
    ret = []

    for d in itertools.combinations(DOMINO, size // 2):
        if sum(sum(map(list, d), [])) == number:
            ret.append(d)

    # shuffle to get shorter expected time to the first solution
    random.shuffle(ret)

    return ret


# choose m disjoint rows or columns from collection
def choose(collection, m, used=set()):
    if m == 0:
        yield []

    else:
        for i, x in enumerate(collection):
            u = used | set(x)
            dj = [x2 for x2 in collection[i + 1:] if all(y not in u for y in x2)]

            for y in choose(dj, m - 1, u):
                yield [x] + y


# all good and disjoint 2-rows
def good_2_rows(board, size, number):
    good = []
    s = number * 2

    for r in itertools.product(*board):
        if sum(sum(map(list, r), [])) == s:
            good.append(r)

    return choose(good, size // 2)


# given a list of domino and a row, return another row
def compliment(dom_lst, row):
    return (d[0] if row[i] == d[1] else d[1] for i, d in enumerate(dom_lst))


# all single good rows
def good_rows(board, size, number):
    perm = []

    for d in board:
        row1 = set()

        for r in itertools.product(*d):
            if sum(r) == number:
                row1.add(r)

        row1 = list(row1)
        row2 = [tuple(compliment(d, r)) for r in row1]
        perm.append(zip(row1, row2))

    return itertools.product(*perm)


# permute over every rows, then cols
def rotate(board):
    for br in itertools.permutations(board):
        flat = []

        for r in br:
            flat.extend(r)

        flat = zip(*flat)

        for bc in itertools.permutations(flat):
            yield bc


# check if diagonal sum is correct
def check(board, number):
    size = len(board)

    return sum(board[i][i] for i in range(size)) == number and \
        sum(board[i][size - 1 - i] for i in range(size)) == number


def magic_domino(size, number):
    cols = all_cols(size, number)

    # for each board with all good cols
    for b_col in choose(cols, size):

        # for each board with good 2-row
        for b_2_row in good_2_rows(b_col, size, number):

            # for each board with all good rows
            for b_row in good_rows(b_2_row, size, number):

                # for each board over all rows and cols rotations
                for b in rotate(b_row):
                    if check(b, number):
                        return list(zip(*b))


if __name__ == '__main__':
    import itertools

    def check_data(size, number, user_result):

        # check types
        check_container_type = lambda o: any(map(lambda t: isinstance(o, t), (list, tuple)))
        check_cell_type = lambda i: isinstance(i, int)
        if not (check_container_type(user_result) and
                all(map(check_container_type, user_result)) and
                all(map(lambda row: all(map(check_cell_type, row)), user_result))):
            raise Exception("You should return a list/tuple of lists/tuples with integers.")

        # check sizes
        check_size = lambda o: len(o) == size
        if not (check_size(user_result) and all(map(check_size, user_result))):
            raise Exception("Wrong size of answer.")

        # check is it a possible numbers (from 0 to 6 inclusive)
        if not all(map(lambda x: 0 <= x <= 6, itertools.chain.from_iterable(user_result))):
            raise Exception("Wrong matrix integers (can't be domino tiles)")

        # check is it a magic square
        seq_sum_check = lambda seq: sum(seq) == number
        diagonals_indexes = zip(*map(lambda i: ((i, i), (i, size - i - 1)), range(size)))
        values_from_indexes = lambda inds: itertools.starmap(lambda x, y: user_result[y][x], inds)
        if not (all(map(seq_sum_check, user_result)) and  # rows
                all(map(seq_sum_check, zip(*user_result))) and  # columns
                all(map(seq_sum_check, map(values_from_indexes, diagonals_indexes)))):  # diagonals
            raise Exception("It's not a magic square.")

        # check is it domino square
        tiles = set()
        for x, y in itertools.product(range(size), range(0, size, 2)):
            tile = tuple(sorted((user_result[y][x], user_result[y + 1][x])))
            if tile in tiles:
                raise Exception("It's not a domino magic square.")
            tiles.add(tile)

    print("6, 13 ...")
    check_data(6, 13, magic_domino(6, 13))
    print("4, 5 ...")
    check_data(4, 5, magic_domino(4, 5))
    print("4, 18 ...")
    check_data(4, 18, magic_domino(4, 18))

    '''
    '''
    size_and_sum_ranges = [
        [4, range(5, 20)],
        [6, range(13, 24)],
    ]

    import datetime
    print(datetime.datetime.now())

    for size, sum_range in size_and_sum_ranges:
        for desired_sum in sum_range:
            print("{}  size={} sum={}".format(
                datetime.datetime.now(), size, desired_sum))

            user_result = magic_domino(size, desired_sum)
            check_data(size, desired_sum, user_result)

    print(datetime.datetime.now())
    '''
    '''

