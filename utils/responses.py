from django.http import JsonResponse


def is_anonymous_response():
    return JsonResponse({ 'message': 'Вы должный войти или зарегистрироваться.' }, status=401)