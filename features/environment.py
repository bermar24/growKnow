from django.test import Client


def before_scenario(context, scenario):
    """Prepare a Django test client and clear any scenario-specific context.

    This ensures steps that use `context.client` will work and prevents state leaking
    between scenarios.
    """
    context.client = Client()

    # Clear commonly-used context attributes if present
    attrs = [
        'draft_article', 'draft_pk', 'published_article', 'approved',
        'notification_enabled', 'draft_saved', 'db_error_simulated',
        'indexed', 'email_sent', 'login_attempt_success', 'num_drafts',
        'response', 'user'
    ]
    for a in attrs:
        if hasattr(context, a):
            delattr(context, a)


def after_scenario(context, scenario):
    # Tear down client reference
    if hasattr(context, 'client'):
        delattr(context, 'client')

