def post_and_admin(request):
    if request.method == 'POST' and request.user.is_superuser:
        return True
    else:
        return False


def post_and_auth(request):
    if request.method == 'POST' and request.user.is_authenticated:
        return True
    else:
        return False
