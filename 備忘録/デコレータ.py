def test(funk):
    print("test start")

    def wrapper(*args, **kwargs):
        print("wrapper start")
        funk()
        print("wrapper end")

    print("test end")
    return wrapper


@test
def main():
    print("main")


if __name__ == '__main__':
    main()
