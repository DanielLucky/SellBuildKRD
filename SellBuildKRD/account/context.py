import datetime as dt


def year(request):
    """
    Добавляет переменную с текущим годом.
    """
    yearNow = dt.datetime.now().year
    return {'year': yearNow}
