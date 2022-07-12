@LoaValidation
Feature: Validate IFrs17 scenarios

  Background: Pre-Requisites for loading LOA Page
    Given Get demo2_UI webUI Env Details
    Given Launch url

  @unit @webUi @firefox
  Scenario Outline: Validate Run for unit in Firefox
    Given Assign Test Cases <TC> from  Demo2_UI sheet in demo2_testCases
    Then For Demo App2 UI
    Then Take screenshot and naming it as demo2_unit

    Examples:
      | TC                 |
      | Demo2_Unit_Test_01 |


  @regression @webUi @chrome
  Scenario Outline: Validate Run for Regression in chrome
    Given Assign Test Cases <TC> from  Demo2_UI sheet in demo2_testCases
    Then For Demo App2 UI
    Then Take screenshot and naming it as demo2_regression

    Examples:
      | TC                  |
      | Demo2_Regression_01 |