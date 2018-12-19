'''Coplen's main module for CLI execution.'''
from pathlib import Path

import coplen.course as course
from carl import command


def package_dir() -> Path:
    return Path(__file__).parent


def default_lang_file() -> Path:
    return Path(f'{package_dir()}/langs/pt-br.json')


@command
def generate(input_file: Path,
             language: Path = default_lang_file(),
             output: Path = 'plan.tex',
             template: Path = f'{package_dir()}/templates/ufsc.tex'):
    loader = {
        '.json': course.from_json,
        '.toml': course.from_toml,
    }[input_file.suffix]

    course.generate(
        course=loader(input_file),
        lang=language,
        output=output,
        template=template,
    )


if __name__ == '__main__':
    generate.run()
