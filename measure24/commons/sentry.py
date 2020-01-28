from configuration.models import Configuration
import sentry_sdk


class Sentry:

    @staticmethod
    def capture_exception(base_exception):
        if Configuration.objects.first() is None:
            print("Nie skonfigurowano sentry SDK")
        else:
            sentry_sdk.capture_exception(base_exception)

    @staticmethod
    def capture_event(base_event):
        if Configuration.objects.first() is None:
            print("Nie skonfigurowano sentry SDK")
        else:
            sentry_sdk.capture_event(base_event)

    @staticmethod
    def capture_message(base_message):
        if Configuration.objects.first() is None:
            print("Nie skonfigurowano sentry SDK")
        else:

            sentry_sdk.capture_message(base_message)
