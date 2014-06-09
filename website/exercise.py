from functools import wraps

CURRENT_EXERCISE_FILE = 'CURRENT_EXERCISE'

exercises = {}

class Exercise(object):
    def __init__(self, number, description, stop=None):
        self.number = number
        self.description = description
        self.stop = stop

    @property
    def enabled(self):
        current_exercise = get_current()
        if self.stop and current_exercise >= self.stop:
            return False

        return current_exercise >= self.number

    def __str__(self):
        return self.description


def exercise(exercise_number, exercise_name, **kwargs):
    if exercise_number in exercises:
        raise Exception("Cannot redefine exercise (%r, %r)" % (exercise_number, exercise_name))

    exercise = exercises[exercise_number] = Exercise(exercise_number, exercise_name, **kwargs)

    return lambda fn: fn if exercise.enabled else None

class MissingExercise(Exception): pass

def set_current(n):
    if n != 0 and n not in exercises:
        raise MissingExercise()

    with file(CURRENT_EXERCISE_FILE, 'w') as fout:
        fout.write(str(n))

def get_current():
    with file(CURRENT_EXERCISE_FILE) as fin:
        return int(fin.read())
