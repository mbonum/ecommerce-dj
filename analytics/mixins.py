from .signals import OBJECT_VIEWED_SIGNAL


class ObjectViewedMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(ObjectViewedMixin, self).get_context_data(*args, **kwargs)
        request = self.request
        instance = context.get("object")
        if instance:
            OBJECT_VIEWED_SIGNAL.send(
                instance.__class__, instance=instance, request=request
            )
        return context
