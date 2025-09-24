wagtail for transera site
=========================

## Test Data

To add test data, run the following manage commands:

```shell
python manage.py seed_merchants --count 50
```

## Build

After model change, migration needs to be executed:

```shell
python manage.py makemigrations && \
python manage.py migrate
```

## Environment Checklist

Check venv directory:

```shell
python -c "import sys; print(sys.prefix)"
```

Check installed packages:

```shell
python -m pip list
```