from django.shortcuts import render

a = []
counter = 1


def history_view(request):
    return render(request, 'history.html', context={'a': a})


def index_view(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        context = {
            'numbers': request.POST.get('numbers')
        }
    try:
        numbers = list(map(int, request.POST.get('numbers').split()))

        check = Check(numbers)
        if check.first_check():
            result = check.first_check()
        else:
            result = check.guess_numbers()
        amount = {"answer": result}
        context.update(dict(amount))
        return render(request, 'index.html', context)

    except ValueError:
        error = 'Это не число. Введите числа!'
    except IndexError:
        error = 'Вы Ввели Пустую строку'
    amount = {"answer": error}
    context.update(dict(amount))
    return render(request, 'index.html', context)


class Check:
    def __init__(self, numbers) -> None:
        self.secret_nums = [1, 3, 2, 7]
        self.numbers = numbers

    def first_check(self):
        for i in self.numbers:
            if i > 9 or i < 0:
                return " Число должно быть больше 0 или меньше 9"
            a = set(self.numbers)
            if len(a) < 4:
                return " Длина меньше 4 символов"
            if len(a) > 4:
                return " Длина больше 4 символов"

    def guess_numbers(self):
        bulls = 0
        cows = 0
        global counter
        if self.numbers == self.secret_nums:
            a.append([counter, 4, 0])
            counter = 1
            return " Вы угадали!"
        else:
            for i in range(len(self.secret_nums)):
                if self.secret_nums[i] == self.numbers[i]:
                    bulls += 1
                elif self.numbers[i] in self.secret_nums:
                    cows += 1

            a.append([counter, bulls, cows])
            counter += 1
            return f" Ты получил {bulls} Быков, {cows} Коров"
