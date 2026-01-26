def add_matrices():
    try:
        n = int(input())
        if n <= 2:
            print("Error!")
            return
        a = [list(map(int, input().split())) for _ in range(n)]
        b = [list(map(int, input().split())) for _ in range(n)]

        for row in a + b:
            if len(row) != n:
                print("Error!")
                return

        for i in range(n):
            row = [str(a[i][j] + b[i][j]) for j in range(n)]
            print(' '.join(row))
    except Exception as e:
        print("Error!")

add_matrices()