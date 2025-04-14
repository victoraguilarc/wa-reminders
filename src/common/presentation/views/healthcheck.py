from django.http import JsonResponse


def healthcheck(_):
    return JsonResponse(
        {
            'name': 'xiberty-api',
            'status': 'OK',
        }
    )
