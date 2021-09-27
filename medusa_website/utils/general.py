from typing import Dict


def traces_sampler(sampling_context: Dict):
    # https://docs.sentry.io/platforms/python/guides/django/configuration/sampling/
    # Always inherit parent
    if sampling_context["parent_sampled"] is not None:
        return sampling_context["parent_sampled"]
    if sampling_context.get("wsgi_environ", {}).get("PATH_INFO") == "/martor/markdownify/":
        return 0.0
    return 1.0
