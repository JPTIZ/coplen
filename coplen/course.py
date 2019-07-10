'''Course plan generator library.'''
import json
import re
from enum import Enum
from pathlib import Path
from typing import NamedTuple, List, Dict, TypeVar

import pytoml as toml
from jinja2 import Environment, FileSystemLoader


MultilineString = TypeVar('MultilineString', str, List[str])


class Month(Enum):
    '''Year's month.'''
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


class Topic(NamedTuple):
    '''A single topic from the course plan.'''
    title: str
    duration: int
    items: List[str]
    extra_items: List[str] = []


class Goals(NamedTuple):
    '''Course general and specific goals.'''
    general: str
    specific: List[str]


class Course(NamedTuple):
    '''A full course plan definition.'''
    kind: str
    title: str
    hours: Dict[str, int]
    start: Month
    end: Month
    year: int
    targets: List[str]
    requires: List[str]
    goals: Goals
    topics: List[Topic]
    schedule: List[str]
    references: List[str]


def lookahead(iterable):
    '''
    Creates and iterable that yields values and a flag indicating if there's
    more values to iter.
    '''
    it = iter(iterable)
    prev = next(it)
    for val in it:
        yield prev, True
        prev = val
    yield prev, False


def save(text: str, output: Path):
    with open(output, 'w') as f:
        f.write(text)


def multiline_str(original: MultilineString) -> str:
    '''
    If original is a list of strings, then joins them. If not, just return
    it imediatly calling `str` on it.
    '''
    if isinstance(original, List):
        return ''.join(original)
    return str(original)


def mdfy(text: str) -> str:
    SUBS = [
        (r'_(.*?)_', r'\\textit{\1}'),
        (r'\*(.*?)\*', r'\\textbf{\1}'),
        (r'`(.*?)`', r'\\texttt{\1}'),
    ]

    for pattern, replace in SUBS:
        text = re.sub(pattern, replace, text)

    return text


def from_json(path: Path) -> Course:
    '''Creates a `coplen.Course` instance from a given JSON file.'''
    with open(path) as f:
        data = json.load(f)

    return Course(
        kind=data['kind'],
        title=data['title'],
        hours=data['hours'],
        start=str(data['start']),
        end=str(data['end']),
        year=data['year'],
        targets=data['targets'],
        requires=data['requires'],
        goals=Goals(
            general=multiline_str(data['goals']['general']),
            specific=map(multiline_str, data['goals']['specific']),
        ),
        topics=[
            Topic(
                title=title,
                duration=topic['duration'],
                items=topic['items'],
            ) for title, topic in data['topics'].items()],
        schedule=data['schedule'],
        references=data['references'],
    )


def from_toml(path: Path) -> Course:
    '''Creates a `coplen.Course` instance from a given TOML file.'''
    with open(path) as f:
        data = toml.load(f)

    about = data['about']
    duration = data['duration']
    topics = data['topics']
    goals = data['goals']
    schedule = data.get('schedule', about.get('schedule', None))

    for topic in topics:
        topic['items'] = [mdfy(item) for item in topic['items']]

    goals = Goals(
        general=multiline_str(goals['general']),
        specific=map(mdfy, map(multiline_str, goals['specific'])),
    )

    return Course(
        kind=about['kind'],
        title=about['title'],
        hours={'theoretical': duration['theoretical'],
               'practice': duration['practice']},
        start=str(duration['start-month']),
        end=str(duration['end-month']),
        year=duration['year'],
        targets=about['targets'],
        requires=about['requires'],
        goals=goals,
        topics=[
            Topic(**topic) for topic in topics],
        schedule=schedule,
        references=about.get('references', ''),
    )


def generate(course,
             template: Path,
             lang='langs/pt-br.json',
             output: str = 'output.tex'):
    '''Generates course plan with given template.'''
    with open(lang) as f:
        lang = json.load(f)

    latex_env = Environment(
                    block_start_string='\BLOCK{',
                    block_end_string='}',
                    variable_start_string='\VAR{',
                    variable_end_string='}',
                    comment_start_string='\#{',
                    comment_end_string='}',
                    line_statement_prefix='%%',
                    line_comment_prefix='%#',
                    trim_blocks=True,
                    autoescape=False,
                    loader=FileSystemLoader([
                            template.parent.resolve(),
                            f'{Path(__file__).parent}/templates',
                        ])
                )
    latex_env.filters['lookahead'] = lookahead

    print(
        f'Generating {output}...\n'
        f'    Template: {template.resolve()}'
    )

    template = latex_env.get_template(template.name)
    save(template.render(course=course, lang=lang), output)
