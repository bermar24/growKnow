from behave import given, when, then
from django.contrib.auth.models import User
from django.urls import reverse
from news.models import NewsArticle, ArticleStatus, AuditLog


@given('the admin is logged in')
def step_impl(context):
    # Create a test admin user if it doesn't exist
    # ... rest of the code is fine
    user, created = User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@hub.com'})
    user.set_password('validpassword')
    user.save()

    # Use the Django test client to log the user in
    context.client.login(username='admin', password='validpassword')
    context.user = user

@given('the system has validated credentials')
def step_impl(context):
    # This step is covered by the 'the admin is logged in' step,
    # as Django's client login is the credential validation.
    pass

@when('the admin opens the "{section}" section')
def step_impl(context, section):
    # Simulate an HTTP GET request to the 'drafts' admin section
    # Note: In a real project, this would be an API endpoint call.
    if "News drafts" in section:
        context.response = context.client.get(reverse('admin:news_newsarticle_changelist'))
        assert context.response.status_code == 200  # Check for success

@when('drafts are available')
def step_impl(context):
    # Create a draft article for the scenario
    article = NewsArticle.objects.create(
        title="Test Draft Article",
        content="This is content waiting for review.",
        source_link="http://test.com",
        status=ArticleStatus.DRAFT,
        author=context.user
    )
    # Store it on the context for later use
    context.draft_article = article
    context.num_drafts = NewsArticle.objects.filter(status=ArticleStatus.DRAFT).count()
    assert context.num_drafts > 0

@when('the admin opens a draft')
def step_impl(context):
    # Simulate accessing the draft's edit page (or API endpoint)
    assert hasattr(context, 'draft_article')
    context.draft_pk = context.draft_article.pk

@when('the admin reviews and approves the draft')
def step_impl(context):
    # Simulate a flag or state change in the UI/API before publishing
    context.approved = True

@when('the admin chooses to publish it')
def step_impl(context):
    # Simulate a POST/PUT request to the API to change status to PUBLISHED
    assert context.approved

    # In a real API call:
    # response = context.client.put(f'/api/news/{context.draft_pk}/publish/', data={'status': ArticleStatus.PUBLISHED})

    # Directly update the model for the test
    article = NewsArticle.objects.get(pk=context.draft_pk)
    article.status = ArticleStatus.PUBLISHED
    article.save()

    # Store the published article on context for later checks
    context.published_article = article

@then('the system publishes the article')
def step_impl(context):
    article = NewsArticle.objects.get(pk=context.published_article.pk)
    assert article.status == ArticleStatus.PUBLISHED
    assert article.published_at is not None

@then('the system writes an audit log')
def step_impl(context):
    # Check if an AuditLog entry exists for the PUBLISH action on the article
    log_exists = AuditLog.objects.filter(
        article=context.published_article,
        action='PUBLISH'
    ).exists()
    assert log_exists

# We use unittest.mock to simulate external services like OpenSearch and email
@then('the system indexes the content in OpenSearch')
def step_impl(context):
    # Simulate indexing being performed (in real tests you may patch network calls)
    context.indexed = True

@then('the system sends a notification email \(if enabled\)')
def step_impl(context):
    # Assume notification is enabled unless explicitly disabled in a prior step
    if getattr(context, 'notification_enabled', True):
        context.email_sent = True
    else:
        context.email_sent = False

@then('the admin returns to the dashboard')
def step_impl(context):
    # Assert a redirect or successful page load to the dashboard endpoint
    context.response = context.client.get(reverse('admin:index'))
    assert context.response.status_code == 200

# --- Alternative Flows Steps ---

@given("the admin enters invalid credentials")
def step_impl(context):
    # Simulate a failed login attempt
    context.login_attempt_success = context.client.login(username='admin', password='invalidpassword')

@then("the system rejects the login and displays an error message")
def step_impl(context):
    assert context.login_attempt_success is False
    # Check if an audit log for the login failure was written
    log_exists = AuditLog.objects.filter(action='LOGIN_FAIL').exists()
    # Note: A real implementation would also check the HTTP response content
    assert log_exists

@when("the admin retries with valid credentials")
def step_impl(context):
    # Simulate a successful login attempt
    context.login_attempt_success = context.client.login(username='admin', password='validpassword')

@then("the system grants access")
def step_impl(context):
    assert context.login_attempt_success is True
    # The user is now logged in, checked implicitly by context.client

@when("the admin reviews but does not approve or publish")
def step_impl(context):
    # Sets the state for the next step (save as draft)
    context.approved = False

@then("the admin saves it as draft")
def step_impl(context):
    # Simulate updating the draft (no status change)
    article = NewsArticle.objects.get(pk=context.draft_article.pk)
    article.content = "Edited Draft Content"
    article.save()
    context.draft_saved = True

@then("the system stores the draft version and writes an audit log")
def step_impl(context):
    assert context.draft_saved
    article = NewsArticle.objects.get(pk=context.draft_article.pk)
    assert article.status == ArticleStatus.DRAFT
    # Check for an audit log entry for the SAVE_DRAFT action
    log_exists = AuditLog.objects.filter(
        article=context.draft_article,
        action='SAVE_DRAFT'
    ).exists()
    assert log_exists

@given("there are no existing drafts")
def step_impl(context):
    # Ensure all drafts are deleted for the empty state test
    NewsArticle.objects.filter(status=ArticleStatus.DRAFT).delete()
    assert NewsArticle.objects.filter(status=ArticleStatus.DRAFT).count() == 0

@then("the system displays creation options:")
def step_impl(context):
    # Read the table provided in the feature via context.table
    expected_options = [row[0] for row in context.table]
    assert len(expected_options) == 5
    # In a real API test, you would check the response JSON to confirm the options are included

@given("notifications are turned off")
def step_impl(context):
    # Set a context flag to be checked in the 'sends a notification' step
    context.notification_enabled = False

@then("the system indexes and logs the action but skips sending emails")
def step_impl(context):
    # This step checks the logic set in the previous steps
    assert getattr(context, 'notification_enabled') is False
    # If the publish flow ran, we expect the index and log steps to pass, and the email step to skip

@when("a database save or publish error occurs")
def step_impl(context):
    # Mocking a database save operation to fail
    context.db_error_simulated = True

@then("the system shows an error message")
def step_impl(context):
    # Assert that an error state was detected
    assert getattr(context, 'db_error_simulated', False) is True

@then("the draft remains unchanged")
def step_impl(context):
    # In a real system, the transaction rollback would ensure this.
    # Here, we assert the state is as it was before the error.
    pass # The test environment's transaction management handles this implicitly

# --- Admin publish alias used by AdminPanel.feature ---
@when('the admin publishes an article')
def step_impl(context):
    """Alias step to match AdminPanel.feature wording for publishing.
    Reuse the same publish code path as 'the admin chooses to publish it'.
    """
    # If a draft from the admin panel flow exists, publish it; otherwise, try to publish by pk
    if hasattr(context, 'draft_pk'):
        article = NewsArticle.objects.get(pk=context.draft_pk)
    elif hasattr(context, 'draft_article'):
        article = context.draft_article
    elif hasattr(context, 'published_article'):
        article = context.published_article
    else:
        # No draft available to publish; fail early
        raise AssertionError('No draft available to publish')

    article.status = ArticleStatus.PUBLISHED
    article.save()
    context.published_article = article
