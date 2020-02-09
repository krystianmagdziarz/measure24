from configuration.models import Configuration
import sentry_sdk


class Sentry:

    init = False

    @staticmethod
    def init_sentry():
        config = Configuration.get_solo()
        if config.sentry_sdk:
            if not Sentry.init:
                sentry_sdk.init(config.sentry_sdk)
                Sentry.init = True
            return True
        else:
            print("Nie skonfigurowano sentry SDK")
            return False

    @staticmethod
    def capture_exception(base_exception):
        if Sentry.init_sentry():
            sentry_sdk.capture_exception(base_exception)

    @staticmethod
    def capture_event(base_event):
        if Sentry.init_sentry():
            config = Configuration.get_solo()
            if config.capture_event:
                sentry_sdk.capture_event(base_event)

    @staticmethod
    def capture_message(base_message):
        if Sentry.init_sentry():
            config = Configuration.get_solo()
            if config.capture_event:
                sentry_sdk.capture_message(base_message)
