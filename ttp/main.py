#!/usr/bin/env python3
import click, arrow
import os, sys, collections
from appdirs import user_config_dir
from pathlib import Path
config_dir = Path(user_config_dir("ttp"))
timefmt = 'YYYY-MM-DD HH:mm ZZ'
trackingStartMsg = "started-tracking ---------------------"

#Set up config dir
if not config_dir.exists():
    config_dir.mkdir()
if not (config_dir/"projects").exists():
    (config_dir/"projects").mkdir()
if not (config_dir/"templates").exists():
    (config_dir/"templates").mkdir()
if not (config_dir/"projects/default.log").exists():
    (config_dir/"projects/default.log").touch()
if not (config_dir/"project.log").is_symlink():
    (config_dir/"project.log").symlink_to("projects/default.log")

@click.group()
def cli():
    pass

@cli.command()
def stretch():
    """Move the last task to now.
    """
    #Why don't we do this using seek? It is a mystery.
    # My theory is that os-primitives for files are 
    # inconsistant between os's...
    with (config_dir/"project.log").open() as f:
        lines = f.readlines()
        date,msg = strpLogLine(lines[-1])
    with (config_dir/"project.log").open("w") as f:
        for line in lines[:-1]:
            f.write(line)
        add(msg)

Task = collections.namedtuple('Task', 'msg span start end week')

def strpLogLine(line):
    date = arrow.get(line,timefmt)
    msg = line.replace(date.format(timefmt),"")
    msg = msg.strip()
    return date, msg

def project_report_data():
    import math
    start=None
    firstWeek=None
    with (config_dir/"project.log").open() as f:
        for index, line in enumerate(f.readlines()):
            if not line.strip():
                continue
            index = index+1
            date, msg = strpLogLine(line)
            if not firstWeek:
                firstWeek = date.floor("week")
            if msg == trackingStartMsg:
                start=date
                continue
            assert start, f"error processing {line} at {index}, tracking was never started."
            week = date-firstWeek
            week = math.ceil(week.days / 7)
            span = date-start
            start = date
            yield Task(
                msg=msg,
                start=start,
                end=date,
                span=span,
                week=week,
            )

def get_dynamic_templates(ctx, args, incomplete):
    paths = (config_dir/"templates").iterdir()
    return [i.name for i in paths if incomplete in i.name]

def setup_jinja2_env():
    import jinja2
    loader = jinja2.ChoiceLoader([
        jinja2.FileSystemLoader(str(config_dir/"templates")),
        jinja2.PackageLoader('ttp'),
    ])
    jinja2_env = jinja2.Environment(loader=loader)
    return jinja2_env

@cli.command()
@click.option('-a','--all','all_', help="Prints full paths.",is_flag=True)
def list_templates(all_):
    """Tells you what templates are available
    """
    env = setup_jinja2_env()
    templates = env.list_templates()
    if all_:
        for template in templates:
            template = env.get_template(template)
            print(template.filename)
    else:
        print(*templates)

@cli.command()
@click.option('-f','--from','from_', help="Start date for report",default=None)
@click.option('-t','--to', help="End date for report",default=None)
@click.option('-w','--week', help="Generate a report for only a specific week",default=None, type=int)
@click.option('-t','--template',type=click.STRING,autocompletion=get_dynamic_templates,default="default.md")
def report(from_,to,week,template):
    """Show a report.
    """
    import dateparser, jinja2
    reportData = project_report_data()
    if from_:
        from_=dateparser(from_)
        reportData = (i for i in reportData if i.start>from_)
    if to:
        to=dateparser(to)
        reportData = (i for i in reportData if i.start<to)
    if week:
        reportData = (i for i in reportData if i.week == week)
    reportData= list(reportData)
    assert reportData, "No tasks to report in that range"
    env = setup_jinja2_env()
    try:
        templateInstance = env.get_template(template)
    except jinja2.exceptions.TemplateNotFound:
        print(f"Can't find a template named `{template}`.")
        print("Try one of the following.")
        print(*env.list_templates())
        sys.exit(1)

    rendered = templateInstance.render(
        #Utility functions
        round = round,
        #Actual data
        start = from_ or reportData[0].start.floor("week"),
        end = to or reportData[-1].start.ceil("week"),
        week = week,
        project = (config_dir/"project.log").resolve().stem,
        total = sum((i.span.seconds for i in reportData)),
        tasks = reportData,
    )
    if sys.stdout.isatty():
        import pygments
        from pygments.lexers import guess_lexer_for_filename
        from pygments.formatters import TerminalFormatter
        lexer = guess_lexer_for_filename(template,rendered)
        print(pygments.highlight(rendered,lexer,TerminalFormatter()))
    else:
        print(rendered)

@cli.command()
@click.argument('task',nargs=-1)
def add(task):
    """Add a task when you have finished working on it
    """
    task = " ".join(task)
    now = arrow.now()
    timestr = now.format(timefmt)
    with (config_dir/"project.log").open("a") as f:
        f.write(f"{timestr} {task}\n")

@cli.command()
def edit():
    """Edit the log with $EDITOR or nano.
    """
    EDITOR = os.environ.get('EDITOR','nano')
    from subprocess import call
    call([EDITOR, (config_dir/"project.log")])

@cli.command()
def start():
    """Start tracking your time.
    """
    now = arrow.now()
    timestr = now.format(timefmt)
    with (config_dir/"project.log").open("a") as f:
        f.write(timestr+" "+trackingStartMsg+"\n")

def get_dynamic_projects(ctx, args, incomplete):
    paths = (config_dir/"projects").iterdir()
    return [i.stem for i in paths if incomplete in i.stem]

@cli.command()
@click.option('--create', help="Create this project if it doesn't already exist",is_flag=True)
@click.argument('project',nargs=-1,type=click.STRING, autocompletion=get_dynamic_projects)
def project(project, create):
    """Start using a specific project.
    """
    project=" ".join(project)
    newProject = Path("projects")/(project+".log")
    projectPath = (config_dir/"project.log")
    if create:
        if (config_dir/newProject).exists():
            print(f"project already exists, not creating")
        (config_dir/newProject).touch()
    if not (config_dir/newProject).exists():
        print(f"{project} does not exist, try running with `--create`. Or maybe you mispelled it?")
        sys.exit(1)

    err = f"Current project at `{config_dir/'project.log'}` is not a symlink, refusing to overwrite"
    assert projectPath.is_symlink(), err
    projectPath.unlink()
    projectPath.symlink_to(newProject)
    print(f"Switched to {project}")

if __name__ == '__main__':
    cli()
