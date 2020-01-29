from configuration.models import Configuration
import sentry_sdk


class Sentry:
    @staticmethod
    def init_sentry(init=True):
        config = Configuration.get_solo()
        if config.sentry_sdk and init:
            sentry_sdk.init(config.sentry_sdk)
        return config.sentry_sdk

    @staticmethod
    def capture_exception(base_exception):
        if Sentry.init_sentry(init=False) is None:
            print("Nie skonfigurowano sentry SDK")
        else:
            sentry_sdk.capture_exception(base_exception)

    @staticmethod
    def capture_event(base_event):
        if Sentry.init_sentry(init=False) is None:
            print("Nie skonfigurowano sentry SDK")
        else:
            sentry_sdk.capture_event(base_event)

    @staticmethod
    def capture_message(base_message):
        if Sentry.init_sentry(init=False) is None:
            print("Nie skonfigurowano sentry SDK")
        else:
            sentry_sdk.capture_message(base_message)
