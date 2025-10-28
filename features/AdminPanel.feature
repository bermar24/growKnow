Feature: Admin Panel - Review, Edit, and Publish News Drafts
  As an admin
  I want to manage news drafts
  So that I can review, edit, publish, or save them

  Background:
    Given the admin is logged in
    And the system has validated credentials

  # --- Basic Flow ---
  Scenario: Admin reviews and publishes a draft
    When the admin opens the "News drafts" section
    And drafts are available
    And the admin opens a draft
    And the admin reviews and approves the draft
    And the admin chooses to publish it
    Then the system publishes the article
    And the system indexes the content in OpenSearch
    And the system writes an audit log
    And the system sends a notification email (if enabled)
    And the admin returns to the dashboard

  # --- Alternative Flows ---
  Scenario: Invalid login
    Given the admin enters invalid credentials
    Then the system rejects the login and displays an error message
    When the admin retries with valid credentials
    Then the system grants access

  Scenario: Admin saves as draft instead of publishing
    When the admin opens a draft
    And the admin reviews but does not approve or publish
    Then the admin saves it as draft
    And the system stores the draft version and writes an audit log

  Scenario: Empty State - no drafts exist
    Given there are no existing drafts
    When the admin opens the "News drafts" section
    Then the system displays creation options:
      | Option                     |
      | Import latest automation output |
      | Generate now               |
      | Create manual draft        |
      | Duplicate last published   |
      | Adjust filters             |

  Scenario: Notification disabled
    Given notifications are turned off
    When the admin publishes an article
    Then the system indexes and logs the action but skips sending emails

  Scenario: System failure during publishing
    When a database save or publish error occurs
    Then the system shows an error message
    And the draft remains unchanged