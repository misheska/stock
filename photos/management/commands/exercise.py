from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.test.utils import get_runner

from website import exercise

class Command(BaseCommand):
    args = "[exercise_number]"
    help = "Shows the current exercise, or sets it if passed an exercise number."

    def handle(self, *args, **options):
        if len(args) > 1:
            raise CommandError("Too many arguments.")

        # Use test runner to make sure test files are imported
        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        test_runner.build_suite(None)

        if len(args) == 1:
            try:
                exercise_number = int(args[0])
            except ValueError:
                raise CommandError("Please pass a validly formatted integer.")

            try:
                exercise.set_current(exercise_number)
            except exercise.MissingExercise:
                raise CommandError("No exercise number {} found.".format(exercise_number))
        else:
            exercise_number = exercise.get_current()

        if exercise_number:
            print "Current Exercise ({}): {}".format(exercise_number, exercise.exercises[exercise_number])
        else:
            print "Not exercise currently enabled."






