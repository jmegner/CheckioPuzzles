'''
author: Jacob Egner
date: 2015-08-03
island: scientific expedition

puzzle URLs:
http://www.checkio.org/mission/math-ghost/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-math-ghost

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


def predict_ghost(vals):
    return 2 * vals[-1] - vals[-2]


if __name__ == '__main__':
    from random import choice, random
    import math
    TESTS_QUANTITY = 30
    SCORE_DIST = 0.1

    def generate_formula(prob_x=0.5, prob_bracket=0.2, prob_trig=0.25):
        formula = "x"
        for _ in range(15):
            operation = choice(["+", "-", "*", "/"])
            formula += operation
            if random() < prob_x:
                formula += "x"
            else:
                formula += str(round(random() * 10, 3))
            if random() < prob_bracket:
                formula = "(" + formula + ")"
            if random() < prob_trig:
                formula = "math." + choice(["sin", "cos"]) + "(" + formula + ")"
        return formula
    
    def calculate_score(f):
        score = 0
        count = 0
        while count < TESTS_QUANTITY:
            formula_x = generate_formula()
            values = []
            for x in range(1, 12):
                try:
                    i = round(eval(formula_x), 3)
                    values.append(i)
                except (OverflowError, ZeroDivisionError):
                    break
            else:
                if abs(max(values) - min(values)) >= 1:
                    score_distance = (max(values) - min(values)) * SCORE_DIST
                    user_result = f(values[:-1])
                    distance = abs(user_result - values[-1])
                    if distance < score_distance:
                        score += round(100 * ((score_distance - distance)
                            / score_distance))
                    count += 1
        print("Total score: {}".format(score))
        return score

    calculate_score(predict_ghost)

