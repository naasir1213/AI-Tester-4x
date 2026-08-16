Feature: Salesforce Login

  As a Salesforce user
  I want to authenticate through the login page
  So that access is granted only with valid credentials

  @ui @login @smoke @positive
  Scenario: Login using valid Salesforce credentials
    Given the user is on the Salesforce login page
    When the user logs in using valid Salesforce credentials
    Then the user should be successfully authenticated

  @ui @login @negative
  Scenario: Login using invalid Salesforce credentials
    Given the user is on the Salesforce login page
    When the user logs in using invalid Salesforce credentials
    Then an authentication error message should be displayed
