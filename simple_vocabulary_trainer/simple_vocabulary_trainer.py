"""Simple Vocabulary Trainer

This is a simple version for a vocabulary trainer. Simple means that this
script only consists of functions, no gui-applycation, no data base, no in-app
vocaulary input, no evaluation of the sessions ,and no statistical evaluation
of all words.

Usage
-----
The user have to add vocabulary lists manually by writing txt-files into the
subdirecory **lessons**. Each line in such a file looks like following:
"english word,german word".
After you have started the vocabulary trainer you just have to follow the
prompts.

Author
------
cjteclab
"""
import os
from typing import List, Dict
from os import listdir


def get_available_lessons() -> Dict:
    """Read files in folder and returns list of files.

    Funcions reads all files in the subdirectory **lessons**.

    Returns
    -------
    dict of {int : str}
        Items consists of lesson number and lesson name.
    """
    return dict(enumerate([file for file in listdir('lessons')]))


def get_selection() -> List:
    """Ask for lessons and returns selection.

    Returns
    -------
    list of {int}
        All the numbers of lessons user selected.
    """
    selection_string = input('''Please enter the lesson numbers you want to
                             learn (comma separated: 1,2,3): ''')
    return [int(x) for x in selection_string.split(',') if x.strip().isdigit()]


def read_lesson_words(lesson: str) -> Dict:
    """Read words in selected file.

    Parameters
    ----------
    lessons : str
        Representation of a lesson file in the subdirectory *lessons**.

    Returns
    -------
    dict of {str : str}
        Items consists of english word : german word.
    """
    lesson_words = {}
    with open("lessons/" + lesson) as file:
        for line in file:
            line = line.strip()
            (english, german) = line.split(',')
            lesson_words[english] = german
    return lesson_words


def get_session_words(selection: List, available_lessons: Dict) -> Dict:
    """Combine all lesson words into a dictionary.

    Parameters
    ----------
    selection : list of {int}
        List numbers the user selected by get_selection().
    available_lessons : dict of {int : str}
        Items consists of lesson number and lesson name.

    Returns
    -------
    dict of {str : str}
        Items consist of english word : german word.
    """
    session_words = {}
    for number in selection:
        session_words.update(read_lesson_words(available_lessons[number]))
    return session_words


def clear_output():
    """Clear Python shell"""
    os.system('cls' if os.name == 'nt' else 'clear')


def run_session(session_words: Dict):
    """Run session and query words.

    Parameters
    ----------
    session_words : dict of {str : str}
        Items consist of english word : german word.
    """
    clear_output()
    for english, german in session_words.items():
        translation = input(f'{german} : ')
        if english == translation:
            print('Correct')
        else:
            print(f'False - correct word: {english}')


def main():
    """Flow of the  main script."""
    print('Hello to the Easy Vocaulary Trainer\n')
    while True:
        print('Available lessons:')
        available_lessons = get_available_lessons()
        for number, lesson in available_lessons.items():
            print(f'{number}: {lesson}')
        print()
        selection = get_selection()
        session_words = get_session_words(selection, available_lessons)
        while True:
            run_session(session_words)
            decision_1 = input('Do you want to repeat this session (y/n)? ')
            if decision_1 == 'n':
                break
        decision_2 = input('Do you want to make a new session (y/n)? ')
        if decision_2 == 'n':
            break
    print('Have a nice day!')


if __name__ == "__main__":
    main()
