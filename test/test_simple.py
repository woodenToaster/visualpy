def test_variables(arg_one):
    x = arg_one
    y = arg_one
    z = x + y

    def another_func(z):
        print(z)
    another_func(z)

test_variables(6)
