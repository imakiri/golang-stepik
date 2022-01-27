from hstest import StageTest, TestedProgram, CheckResult, dynamic_test

class Test(StageTest):
	@dynamic_test
	def test0(self) -> CheckResult:
		program = TestedProgram()

		reply = program.start().strip().lower().split("\n")
		if "enter command and data:" not in reply[0]:
			return CheckResult.wrong('The program should ask user for a command\nThis error happened at the very beginning of the program execution')

		reply = program.execute("create This is my first record!").strip().lower().split("\n")
		if "[ok] the note was successfully created" not in reply[0]:
			return CheckResult.wrong('The program should inform the user about the successful creation of the note')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("list").strip().lower().split("\n")
		if "[info] 1: this is my first record!" not in reply[0]:
			return CheckResult.wrong('')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong("The program should ask user for a command\nThe program shouldn't print empty notes")

		reply = program.execute("clear").strip().lower().split("\n")
		if "[ok] all notes were successfully deleted" not in reply[0]:
			return CheckResult.wrong('The program should inform the user about the successful deletion of notes')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("list").strip().lower().split("\n")
		if "" not in reply[0]:
			return CheckResult.wrong('')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong("The program should ask user for a command\nThe program shouldn't print empty notes")

		reply = program.execute("exit").strip().lower().split("\n")
		if "[info] bye!" not in reply[0]:
			return CheckResult.wrong('The program should print the farewell message to the user upon its shutdown')

		return CheckResult.correct()

	@dynamic_test
	def test1(self) -> CheckResult:
		program = TestedProgram()

		reply = program.start().strip().lower().split("\n")
		if "enter command and data:" not in reply[0]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("create This is my first record!").strip().lower().split("\n")
		if "[ok] the note was successfully created" not in reply[0]:
			return CheckResult.wrong('The program should inform the user about the successful creation of the note')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("create This is my second record!").strip().lower().split("\n")
		if "[ok] the note was successfully created" not in reply[0]:
			return CheckResult.wrong('The program should inform the user about the successful creation of the note')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("create This is my third record!").strip().lower().split("\n")
		if "[ok] the note was successfully created" not in reply[0]:
			return CheckResult.wrong('The program should inform the user about the successful creation of the note')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("create This is my forth record!").strip().lower().split("\n")
		if "[ok] the note was successfully created" not in reply[0]:
			return CheckResult.wrong('The program should inform the user about the successful creation of the note')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("create This is my fifth record!").strip().lower().split("\n")
		if "[ok] the note was successfully created" not in reply[0]:
			return CheckResult.wrong('The program should inform the user about the successful creation of the note')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("create This is my sixth record!").strip().lower().split("\n")
		if "[error] notepad is full" not in reply[0]:
			return CheckResult.wrong('The program should inform the user when the internal storage is full')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("list").strip().lower().split("\n")
		if "[info] 1: this is my first record!" not in reply[0]:
			return CheckResult.wrong('')
		if "[info] 2: this is my second record!" not in reply[1]:
			return CheckResult.wrong('')
		if "[info] 3: this is my third record!" not in reply[2]:
			return CheckResult.wrong('')
		if "[info] 4: this is my forth record!" not in reply[3]:
			return CheckResult.wrong('')
		if "[info] 5: this is my fifth record!" not in reply[4]:
			return CheckResult.wrong('')
		if "enter command and data:" not in reply[5]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("clear").strip().lower().split("\n")
		if "[ok] all notes were successfully deleted" not in reply[0]:
			return CheckResult.wrong('The program should inform the user about the successful deletion of notes')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("create This is my sixth record!").strip().lower().split("\n")
		if "[ok] the note was successfully created" not in reply[0]:
			return CheckResult.wrong('The program should inform the user about the successful creation of the note')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("list").strip().lower().split("\n")
		if "[info] 1: this is my sixth record!" not in reply[0]:
			return CheckResult.wrong('')
		if "enter command and data:" not in reply[1]:
			return CheckResult.wrong('The program should ask user for a command')

		reply = program.execute("exit").strip().lower().split("\n")
		if "[info] bye!" not in reply[0]:
			return CheckResult.wrong('The program should print the farewell message to the user upon its shutdown')

		return CheckResult.correct()


if __name__ == '__main__':
	Test().run_tests()
