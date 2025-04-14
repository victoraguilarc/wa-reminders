from django.http import JsonResponse


def healthcheck(_):
    return JsonResponse(
        {
            'name': 'wa-reminders',
            'status': 'OK',
        }
    )
