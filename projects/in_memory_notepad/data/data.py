from projects.in_memory_notepad.testlib.testlib import *

Output_WaitingForMaxNum = Output(
    "Enter the maximum number of notes: ",
    "The program should ask user to enter the maximum number of notes"
)
Output_WaitingForUserInput = Output(
    "Enter command and data: ",
    "The program should ask user for a command"
)
Output_NoteCreated = Output(
    "[OK] The note was successfully created",
    "The program should inform the user about the successful creation of the note"
)
Output_MissingIndex = Output(
    "[Error] Missing index argument",
    "The program should inform the user when it can't find the index argument"
)
Output_MissingNote = Output(
    "[Error] Missing note argument",
    "The program should inform the user when it can't find the note argument"
)
Output_NothingToUpdate = Output(
    "[Error] There is nothing to update",
    ""
)
Output_NothingToDelete = Output(
    "[Error] There is nothing to delete",
    ""
)
Output_ListFull = Output(
    "[Error] Notepad is full",
    "The program should inform the user when the internal storage is full"
)
Output_ListEmpty = Output(
    "[Info] Notepad is empty",
    ""
)
Output_ListCleared = Output(
    "[OK] All notes were successfully deleted",
    "The program should inform the user about the successful deletion of notes"
)
Output_UnknownCommand = Output(
    "[Error] Unknown command",
    "The program should inform the user when it can't recognize the given command"
)
Output_Bye = Output(
    "[Info] Bye!",
    "The program should print the farewell message to the user upon its shutdown"
)

def Output_InvalidIndex(index: str) -> Output:
    return Output(f"[Error] Invalid index: {index}", "")

def Output_IndexOutOfBoundaries(index: int, upper: int) -> Output:
    return Output(f"[Error] Index {index} is out of the boundaries [0, {upper})", "")

def Output_Updated(index: int) -> Output:
    return Output(f"[OK] The note at index {index} was successfully updated", feedback_noteUpdated)

def Output_Deleted(index: int) -> Output:
    return Output(f"[OK] The note at index {index} was successfully deleted", feedback_noteDeleted)

def Output_Note(index: int, value: str) -> Output:
    return Output(f"[Info] Index {index}: {value}", "")

feedback_command = "The program should print back ONLY the given command and no more"
feedback_printingEmptyNotes = "The program shouldn't print empty notes"
feedback_noteUpdated = "The program should inform the user about the successful update of the note"
feedback_noteDeleted = "The program should inform the user about the successful deletion of the note"

Input_List = Input("list")
Input_Clear = Input("clear")
Input_Exit = Input("exit")


def Input_Create(value: str) -> Input:
    return Input(f"create {value}")

def Input_Update(index: int, value: str) -> Input:
    return Input(f"update {index} {value}")

def Input_Delete(index: int) -> Input:
    return Input(f"delete {index}")

