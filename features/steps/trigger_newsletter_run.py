from behave import given, when, then


@given("the system runs the scheduled n8n workflow")
def run_scheduled_workflow(context):
    # Simulate n8n workflow execution
    print("n8n workflow executed on schedule")


@when("the workflow fetches sources, deduplicates items, extracts key points, classifies and tags news")
def workflow_processes_news(context):
    # Simulate data processing
    print("News sources fetched and processed")


@when("generates a news article draft")
def generate_draft(context):
    context.draft_sent_to_system = True
    print("Draft generated and sent to system")


@then("the draft is sent to the system")
def draft_sent(context):
    assert getattr(context, 'draft_sent_to_system', False), "Draft was not sent to the system"


# --- System intake steps ---
@when("the system stores the draft in the database")
def store_draft(context):
    context.draft_stored = True
    print("Draft stored in database")


@when("indexes the draft for search")
def index_draft(context):
    context.draft_indexed = True
    print("Draft indexed for search")


@when("queues the draft for review")
def queue_draft(context):
    context.draft_queued = True
    print("Draft queued for admin review")


@when("notifies the admin")
def notify_admin(context):
    context.admin_notified = True
    print("Admin notified of new draft")


# --- Admin review and publish steps ---
@when("the admin opens the review link")
def admin_opens_review_link(context):
    assert getattr(context, 'draft_queued', False), "Draft not queued for review"
    print("Admin opened review link")


@when("reviews the draft")
def admin_reviews_draft(context):
    print("Admin is reviewing draft")


@when("approves the draft")
def admin_approves_draft(context):
    context.draft_approved = True
    print("Admin approved draft")


@when("clicks publish")
def admin_publishes_draft(context):
    assert getattr(context, 'draft_approved', False), "Draft not approved"
    context.draft_published = True
    print("Draft published")


@then("the system publishes the article to the website")
def system_publishes_draft(context):
    assert getattr(context, 'draft_published', False), "Draft was not published"
    print("Article is live on website")


@then("logs run metrics including timestamps, items processed, dedupe count, review latency, and publish status")
def log_metrics(context):
    print("Run metrics logged")

