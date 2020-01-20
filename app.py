from random import randint

singles = []
doubles = []
triples = []
throw_outs = []


class Player:
    def __init__(self, name):
        self.previous_score = 0
        self.name = name
        self.scores = []
        self.score_left = 501

    def subtract_score(self, scored):
        self.previous_score = self.score_left
        self.scores.append(scored)
        self.score_left -= scored


# fill up the lists with the possibilities
for num in range(1, 22):
    if num == 21:
        singles.append(25)
        doubles.append(25)
    else:
        singles.append(int(num))
        doubles.append(int(num))
        if num != 21:
            triples.append(int(num))


def get_game_mode(mode):
    switch = {
        "S": [singles],
        "D": [doubles],
        "T": [triples],
        "S, D": [singles, doubles],
        "S, T": [singles, triples],
        "D, T": [doubles, triples],
        "S, D, T": [singles, doubles, triples]
    }
    mode = switch[f"{mode}"]
    return mode


def merge(arr):
    combined_array = []
    index = 1
    for subarr in arr:
        for number in subarr:
            if index == 1:
                combined_array.append(f"S{number}")
            elif index == 2:
                combined_array.append(f"D{number}")
            else:
                combined_array.append(f"T{number}")
        index += 1
    return combined_array


def random_fields():
    # only singles, doubles, or, triples or a combination of all possible options
    modes = ("S", "D", "T", "S, D", "S, T", "D, T", "S, D, T")
    start_game = False
    while not start_game:
        # s is singles, d is doubles and t is triples
        mode = input("What mode ? (s), (d), (t)\n"
                     "Multiple options are possible separated by a comma and space: s, d, t: ").upper()
        total_fields = False if mode not in modes else get_game_mode(mode)
        if total_fields:
            start_game = True
        else:
            print("Enter a valid game mode")
    all_fields = merge(total_fields)
    continue_game = True
    while continue_game:
        three_numbers = ""
        for i in range(3):
            three_numbers += f" {all_fields[randint(0, len(all_fields)-1)]}"
        print(three_numbers)
        choice = input("Three more numbers? (y) or (n):").upper()
        while choice != "Y" and choice != "N":
            choice = input("Three more numbers? (y) or (n):").upper()
        continue_game = False if choice == "N" else True


def five_o_one():
    players = [Player(input("Name Player One? ")), Player(input("Name Player Two? "))]
    player_one_turn = True
    print(f"{players[0].name}: {players[0].score_left} \n"
          f"{players[1].name}: {players[1].score_left}")
    # as long as neither players score reached zero by using a double with the last dart loop continues
    while players[0].score_left != 0 and players[1].score_left != 0:
        old_score = players[0].score_left if player_one_turn else players[1].score_left
        score = int(input(f"{players[0].name if player_one_turn else players[1].name}, Whats your score? "))
        players[0].subtract_score(score) if player_one_turn else players[1].subtract_score(score)
        if players[0].score_left == 0 or players[1].score_left == 0:
            answer = input("was it double out? (y) or (n) :").upper()
            double_out = True if answer == "Y" else False
            print(f"{players[0].score_left if player_one_turn else players[1].score_left} back to previous score")
            if player_one_turn:
                players[0].score_left = 0 if double_out else old_score
            else:
                players[1].score_left = 0 if double_out else old_score
        # when it is not possible to reach zero with a double players score goes back to old score
        elif players[0].score_left <= 1 or players[1].score_left <= 1:
            print(f"{players[0].score_left if player_one_turn else players[1].score_left} back to previous score")
            if player_one_turn:
                players[0].score_left = players[0].previous_score
            else:
                players[1].score_left = players[1].previous_score
        print(f"{players[0].name}: {players[0].score_left} \n"
              f"{players[1].name}: {players[1].score_left}")
        player_one_turn = False if player_one_turn else True
    print(f"{players[1].name if player_one_turn else players[0].name}, Is the winner ")


def multi_nested_loop(matched_num, arr1, arr2, arr3=[]):
    matches = []

    for num1 in arr1:
        a = 'S' if arr1 == singles else 'T'
        for num2 in arr2:
            if arr2 == singles:
                b = 'S'
            elif arr2 == doubles:
                b = 'D'
            else:
                b = 'T'
            # only when three arrays are given
            if len(arr3) != 0:
                for num3 in arr3:
                    c = 'D'
                    n1 = 3 * num1 if arr1 == triples else num1
                    n2 = 3 * num2 if arr2 == triples else num2
                    n3 = 2 * num3
                    total = int(n1) + int(n2) + int(n3)
                    if matched_num == total:
                        order = f"{a}{num1}, {b}{num2}, {c}{num3}"
                        matches.append(order)
            else:
                total = num1 + num2
                if matched_num == total:
                    order = f"{num1}, {num2}"
                    matches.append(order)
    return matches


def possible_outs():
    points_left = int(input("How much point are left? "))
    darts_remaining = int(input("How many darts are left? "))
    possibilities = []
    if points_left in doubles:
        possibilities.append(points_left)
    if darts_remaining == 2:
        if points_left < 71 and len(possibilities) == 0:
            possibilities = multi_nested_loop(points_left, singles, doubles)
        if points_left < 111 and len(possibilities) == 0:
            possibilities = multi_nested_loop(points_left, triples, doubles)
            possibilities2 = multi_nested_loop(points_left, doubles, doubles)
            for number in possibilities2:
                possibilities.append(number)
    elif darts_remaining == 3:
        if points_left < 91 and len(possibilities) == 0:
            possibilities = multi_nested_loop(points_left, singles, singles, doubles)
        if points_left < 136 and len(possibilities) == 0:
            possibilities = multi_nested_loop(points_left, singles, triples, doubles)
        if points_left < 171 and len(possibilities) == 0:
            possibilities = multi_nested_loop(points_left, triples, triples, doubles)
            possibilities2 = multi_nested_loop(points_left, triples, doubles, doubles)
            for number in possibilities2:
                possibilities.append(number)
    for i in possibilities:
        print(i)
