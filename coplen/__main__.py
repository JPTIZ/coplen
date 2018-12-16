'''TODO'''
import os.path

import coplen.course as course
from carl import command


def package_dir():
    return os.path.dirname(__file__)


def default_lang_file():
    return f'{package_dir()}/langs/pt-br.json'


@command
def generate(input_file: str,
             language: str = default_lang_file(),
             output: str = 'plan.tex',
             template: str = f'{package_dir()}/templates/ufsc.tex'):

    course.generate(
        course=course.from_json(input_file),
        lang=language,
        output=output,
        template=template,
    )


generate.run()
