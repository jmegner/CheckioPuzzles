def fibgolf(s, n):
    a, b, c = [2, 1, 1] if 'u' in s else [3, 0, 2] if s == 'perrin' else [0, 1, 1]
    while n:
        [a, b, c] = [b, c, a+b+c] if 'tr' in s else [b, c, a + b] if s[-1] == 'n' else [b, (2 if 'j' in s else 1) * a + (2 if s == 'pell' else 1) * b, c]
        n -= 1
    return a
