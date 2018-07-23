'''Course plan generator library.'''
import json
from enum import Enum
from os.path import abspath
from typing import NamedTuple, List, Dict

from jinja2 import Environment, FileSystemLoader


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


def save(text, output):
    with open(output, 'w') as f:
        f.write(text)


def multiline_str(original):
    '''
    If original is a list of strings, then joins them. If not, just return
    it imediatly.
    '''
    if isinstance(original, str):
        return original
    return ''.join(original)


def from_json(filename: str):
    '''Creates a `coplen.Course` instance from a given json file.'''
    with open(filename) as f:
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
            general=data['goals']['general'],
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


def generate(course,
             template,
             lang='pt-br',
             output: str = 'output.tex'):
    '''Generates course plan with given template.'''
    with open(f'langs/{lang}.json') as f:
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
                    loader=FileSystemLoader(abspath('.'))
                )
    latex_env.filters['lookahead'] = lookahead

    print('Generating TeX...')
    template = latex_env.get_template(template)
    save(template.render(course=course, lang=lang), output)
