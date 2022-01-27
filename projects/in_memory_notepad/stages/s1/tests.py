from hstest import StageTest, TestedProgram, CheckResult, dynamic_test

class Test(StageTest):
	"""

	Можем ли мы обсудить тесты без посредников?

	"""

	@dynamic_test
	def test0(self) -> CheckResult:
		program = TestedProgram()

		reply = program.start().strip().lower().split("\n")
		if "enter command and data:" not in reply[0]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("create This is my first record!").strip().lower().split("\n")
		if "create" not in reply[0]:
			return CheckResult.wrong('The program should print back only the given command and no more')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("create This is my second record!").strip().lower().split("\n")
		if "create" not in reply[0]:
			return CheckResult.wrong('The program should print back only the given command and no more')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("list").strip().lower().split("\n")
		if "list" not in reply[0]:
			return CheckResult.wrong('The program should print back only the given command and no more')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("exit 1098").strip().lower().split("\n")
		if "[info] bye!" not in reply[0]:
			return CheckResult.wrong('The program should print the farewell message to the user upon its shutdown')

		return CheckResult.correct()

	@dynamic_test
	def test1(self) -> CheckResult:
		program = TestedProgram()

		reply = program.start().strip().lower().split("\n")
		if "enter command and data:" not in reply[0]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("2naDI08 U 7 44hM9z6rjymPO15taCIiu4IPs1bS0Lvled3H 3GOJLVjf3PMqzwFA oaFAHpI8bIBw8TzI").strip().lower().split("\n")
		if "2nadi08" not in reply[0]:
			return CheckResult.wrong('The program should print back only the given command and no more')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("XXYMVytHU4VkXCNjvGDKWecsS a0b4zN25fkM1YUCqBAc j7IWjEs8H76du8LUJsZsqi8 5KO6JSd").strip().lower().split("\n")
		if "xxymvythu4vkxcnjvgdkwecss" not in reply[0]:
			return CheckResult.wrong('The program should print back only the given command and no more')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("exit KnaW6dIZVab4iPm0kKYfaKNST fk9Tukrxi3MQbk2hChWNY4Ff oE28ghqzgRGXiH").strip().lower().split("\n")
		if "[info] bye!" not in reply[0]:
			return CheckResult.wrong('The program should print the farewell message to the user upon its shutdown')

		return CheckResult.correct()

	@dynamic_test
	def test2(self) -> CheckResult:
		program = TestedProgram()

		reply = program.start().strip().lower().split("\n")
		if "enter command and data:" not in reply[0]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("FjiOwRPnsHBqfk huhvWL80qqxQciBwFVq8VLPryY").strip().lower().split("\n")
		if "fjiowrpnshbqfk" not in reply[0]:
			return CheckResult.wrong('The program should print back only the given command and no more')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("47BIlQ5gTk 1vLhxNtSciKrmY2PAXcCTPSVnwnZ1e6AalnzqWmulLJ29gChElTucPLS").strip().lower().split("\n")
		if "47bilq5gtk" not in reply[0]:
			return CheckResult.wrong('The program should print back only the given command and no more')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("Zdd2bHG0Iesbwnj4VJ8mTpyxW1NAThaqVA35Jo ").strip().lower().split("\n")
		if "zdd2bhg0iesbwnj4vj8mtpyxw1nathaqva35jo" not in reply[0]:
			return CheckResult.wrong('The program should print back only the given command and no more')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("exit u2UNhwqRxrkuuTUiLnu1hzm9BDEGQbvnNUNSL4PYZ3I6oazK5t0TfSf3RSZL9").strip().lower().split("\n")
		if "[info] bye!" not in reply[0]:
			return CheckResult.wrong('The program should print the farewell message to the user upon its shutdown')

		return CheckResult.correct()


if __name__ == '__main__':
	Test().run_tests()
