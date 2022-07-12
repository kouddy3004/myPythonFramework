@DemoApp1WS
Feature: Validate Straight Line Method Amortization scenarios

  Background: Pre-Requisites for setting details for Straight Line Method Amortization webServices
    Given Get demo1_WebService webServices Env Details


  @unit @webService
  Scenario Outline: Validate Straight Line Amortization Scenarios
    Given Assign Test Cases <TC> from  DemoApp1_WS sheet in demo1_testCases
    Then For Demo App1 WS


    Examples:
      | TC             |
      | TC_Demo1_WS_01 |
      | TC_Demo1_WS_02 |