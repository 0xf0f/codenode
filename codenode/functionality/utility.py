def isplit(string: str, sep):
    start = 0
    sep_length = len(sep)

    while True:
        sep_index = string.find(sep, start)
        if sep_index > -1:
            yield string[start:sep_index]
            start += (sep_index-start) + sep_length
        else:
            break

    yield string[start:]


# if __name__ == '__main__':
#     string = 'asdasd asd asd asdasd asd asd asd asd asd'
#     print(*isplit(string, ' '), sep=',')
