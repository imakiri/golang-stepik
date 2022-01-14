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
Output_EmptyNote = Output(
    "[Error] The note cannot be empty",
    "The program should inform the user about the unsuccessful creation of the note as well as about what caused it (note is an empty string)"
)
Output_ListFull = Output(
    "[Error] The list of notes is full",
    "The program should inform the user about the unsuccessful creation of the note as well as about what caused it (list is full)"
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
    "Bye!",
    "The program should print the farewell message to the user upon its shutdown"
)

feedback_command = "The program should print back ONLY the given command and no more."
feedback_noteUpdated = "The program should inform the user about the successful update of the note"
feedback_noteDeleted = "The program should inform the user about the successful deletion of the note"


def message_noteUpdated(index: int) -> str:
    return f"[OK] The note at index {index} was successfully updated"


def message_noteDeleted(index: int) -> str:
    return f"[OK] The note at index {index} was successfully deleted"
