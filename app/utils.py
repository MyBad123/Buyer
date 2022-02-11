def post_and_admin(request):
    if request.method == 'POST' and request.user.is_superuser:
        return False
    else:
        return True


def post_and_auth(request):
    if request.method == 'POST' and request.user.is_authenticated:
        return True
    else:
        return False
