def logo_filename(instance, filename):
    return 'logo'


def app_information():
    """
    Function to be passed in cache.get_or_set as default callable.

    Just passing App.objects.all().get in would call the method
    App.objects.all, performing a database query (which is intended
    to be avoided by using the cache).

    Just passing App.objects.all in would not perform any query, but
    it would store a QuerySet in the cache, instead of an App instance.
    While this is perfectly manageable, I DO NOT LIKE IT. <3
    """

    from .models import App
    return App.objects.all().get()
