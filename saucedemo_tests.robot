*** Settings ***
Library    SauceDemoLibrary.py

Suite Setup    Start Browser
Suite Teardown    Stop Browser

*** Variables ***
${username}    standard_user
${password}    secret_sauce

*** Test Cases ***

TC01 - Login Test
    Open Saucedemo
    Login    ${username}    ${password}
    Wait For Load

TC02 - Add To Cart And Validate
    Open Saucedemo
    Login    ${username}    ${password}
    Wait For Load
    Add To Cart

TC03 - Full Checkout Flow
    Open Saucedemo
    Login    ${username}    ${password}
    Wait For Load
    Add To Cart
    ${count}    Get Cart Count
    Go To Cart
    Validation Item Count    ${count}
    Proceed To Checkout
    Fill Customer Info    Aru    Don    908765
    Complete Order

    

