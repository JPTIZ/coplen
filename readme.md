coplen
======

About
-----

**Co**urse **Pl**an G**en**erator, used to generate course plans with given
template file.

Simple Example
--------------

A simple example is [here](examples/plan.pdf), to see how it was generated.

Basic Usage
-----------

With `python -m coplen --help`:

```text
usage: __main__.py [-h] [--language LANGUAGE] [--output OUTPUT]
                   [--template TEMPLATE]
                   input_file

positional arguments:
  input_file

optional arguments:
  -h, --help           show this help message and exit
  --language LANGUAGE
  --output OUTPUT
  --template TEMPLATE
```

The **language** comes from a [JSON file](langs/pt-br.json), for translation
purposes. **Template** is a [template file](templates/ufsc.tex) in whatever
format you may want, including TEX, using default Jinja2 syntax.

So, using `examples/plan.json` as an example:

```bash
$ python -m coplen --template templatex/ufsc.tex --output examples/plan.tex examples/plan.json
```

In `examples/` directory, there is a `makefile` to generate the plan PDF:

```bash
$ make -C examples
```

The makefile is configured to generate a file `examples/plan.pdf` using
`xelatex` (you may change on your own), so you can check the result.
