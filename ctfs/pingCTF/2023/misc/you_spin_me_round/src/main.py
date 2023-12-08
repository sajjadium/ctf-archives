import random
import time

from flag import FLAG
from messages import hello, m_task1, m_task2, m_task3, m_correct, m_incorrect

TIME_LIMIT_SEC = 10


def task1(n):
	x = random.randint(100, 10000)
	y = random.randint(1, 100)
	solution = x // y
	m_task1(x, solution, n)
	answer = int(input('Enter what should be under "?" in the task above: '))
	user_solution = x // answer
	if user_solution == solution:
		m_correct()
	else:
		user_solution = f"{x} // {answer} = {user_solution}"
		correct_solution = f"{x} // {y} = {solution}"
		m_incorrect(user_solution, correct_solution)
		exit(1)


def task2(n):
	x = random.randint(100000, 1000000000) / 100
	y = random.randint(1, 100000) / 100
	solution = x % y
	m_task2(x, solution, n)
	answer = float(input('Enter what should be under "?" in the task above: '))
	user_solution = x % answer
	if user_solution == solution:
		m_correct()
	else:
		user_solution = f"{x} % {answer} = {user_solution}"
		correct_solution = f"{x} % {y} = {solution}"
		m_incorrect(user_solution, correct_solution)
		exit(1)


def task3(n):
	x = random.randint(100000, 1000000000) / 100
	y = random.randint(1, 100000) / 100
	solution = x % y
	m_task3(x, y, n)
	user_solution = input('Enter what should be under "?" in the task above: ')
	if user_solution != str(solution) and float(user_solution) == solution and not user_solution.endswith('0'):
		m_correct()
	else:
		opt_text = f'This is a special case! You need to satisfy the following condition to pass it.'
		opt_text += f'\n"{user_solution}" != str({solution}) and float("{user_solution}") == {solution} and not "{user_solution}".endswith("0")'
		m_incorrect(user_solution, solution, opt_text)
		exit(1)


def task4():
	print('START')
	time_start = time.time()
	for i in range(4, 1_000):
		task = random.randint(1, 3)
		eval(f'task{task}({i})')
	time_end = time.time()

	if time_end - time_start > TIME_LIMIT_SEC:
		print('You are too slow!')
		exit(1)


def main():
	# quantum security random seed security layer - impossible to crack on a classical calculators
	seed = random.randint(0, 1_000_000)
	random.seed(seed)
	hello(random.randint(1, 100), random.randint(1, 100))
	task1(1)
	task2(2)
	task3(3)
	print('Good job! :) You proved you are a human!!!\n\n')
	print('However unfortunately this is not enough to get the flag. As friendly as I am, I can only provide the flag to the fellow bots.\n\n')
	print('To prove it you need to solve task 4 in a limited time.\n\n')
	task4()
	print(f'{FLAG=}')


if __name__ == '__main__':
	main()
