from projects.in_memory_notepad.testlib.testlib import *

Output_WaitingForMaxNum = Output(
    "Enter the maximum number of notes: ",
    "The program should ask user to enter the maximum number of notes")
Output_WaitingForUserInput = Output(
    "Enter command and data: ",
    "The program should ask user for a command")
Output_NoteCreated = Output(
    "[OK] The note was successfully created",
    "The program should inform the user about the successfully creation of the note")
Output_ListFull = Output(
    "[Error] The list of notes is full",
    "")
Output_ListCleared = Output(
    "[OK] All notes were successfully deleted",
    "")

feedback_command = "The program should print back ONLY the given command and no more."
feedback_bye = "The program should print the farewell message to the user upon its shutdown"


def message_deleted(index: int):
    return f"[OK] The note at index {index} was successfully deleted"
