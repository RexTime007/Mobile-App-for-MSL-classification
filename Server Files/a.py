from scoop import futures

def square(x):
    return x**2

if __name__ == '__main__':
    values = [1, 2, 3, 4, 5]
    results = list(futures.map(square, values))
    print(results)