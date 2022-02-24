def get_or_create(klass, *args, **kwargs):
    try:
        obj = klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        klass.objects.create(*args, **kwargs)
