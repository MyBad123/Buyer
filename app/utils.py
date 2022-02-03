def post_and_auth(request):
    if request.method == 'POST' and request.user.is_superuser:
        return False
    else:
        return True
