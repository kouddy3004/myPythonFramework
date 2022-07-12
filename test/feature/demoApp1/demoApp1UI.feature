@DemoApp1UI
Feature: Validate Eira UI scenarios

  Background: Pre-Requisites for setting details for Eira UI
    Given Get demo1_UI webUI Env Details
    Given Launch url


  @unit @webUi @firefox
  Scenario Outline: Validate EIRA UI Scenarios
    Given Assign Test Cases <TC> from  DemoApp1_UI sheet in demo1_testCases
    Then For Demo App1 UI
    Then Take screenshot and naming it as demo1

    Examples:
      | TC             |
      | TC_Demo1_UI_01 |

