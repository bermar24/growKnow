Feature: Trigger Newsletter Run (Automation → Review → Publish)
  As an admin
  I want to review and publish automatically generated newsletter drafts
  So that vetted news articles are published efficiently

  Background:
    Given the admin is logged in

  Scenario: Automated newsletter draft generation and publication
    # Automation (n8n)
    Given the system runs the scheduled n8n workflow
    When the workflow fetches sources, deduplicates items, extracts key points, classifies and tags news
    And generates a news article draft
    Then the draft is sent to the system

    # System intake
    When the system stores the draft in the database
    And indexes the draft for search
    And queues the draft for review
    And notifies the admin

    # Admin review and publish
    When the admin opens the review link
    And reviews the draft
    And approves the draft
    And clicks publish
    Then the system publishes the article to the website
    And logs run metrics including timestamps, items processed, dedupe count, review latency, and publish status
