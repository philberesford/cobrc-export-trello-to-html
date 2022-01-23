from invoke import task


@task(aliases=["black"])
def reformat(context):
    context.run("black .")


@task(aliases=["pytest"])
def test(context):
    context.run("pytest gilded_rose_kata_python")


@task(aliases=["pytest_coverage"])
def test_coverage(context):
    context.run("pytest --cov gilded_rose_kata_python")


@task()
def linting(context):
    context.run("pylint gilded_rose_kata_python")
    context.run("mypy gilded_rose_kata_python")


@task()
def build(context):
    reformat(context)
    test(context)
    linting(context)
