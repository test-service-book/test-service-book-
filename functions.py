from random import randint

# функция, которая генерирует код для транзакции,
# пока для того, чтобы менять машины и добавлять работу
def generate_code_for_transaction(l=5):

    res = ''
    for i in range(l):
        res += str(randint(0, 9))

    return res
