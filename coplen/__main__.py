'''TODO'''
import coplen.course as course
from carl import command


@command
def generate(input_file: str,
             language: str = 'pt-br',
             output: str = 'plan.tex',
             template: str = 'templates/ufsc.tex'):

    course.generate(
        course=course.from_json(input_file),
        lang=language,
        output=output,
        template=template,
    )


generate.run()
