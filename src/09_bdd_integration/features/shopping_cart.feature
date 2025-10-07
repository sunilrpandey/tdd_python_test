Feature: Shopping Cart Management
    As a customer
    I want to manage my shopping cart
    So that I can purchase items

    Background:
        Given the shopping cart is empty
        And the following products exist:
            | id    | name           | price |
            | PROD1 | Test Product 1 | 10.00 |
            | PROD2 | Test Product 2 | 20.00 |
            | PROD3 | Test Product 3 | 30.00 |

    Scenario: Add item to cart
        When I add product "PROD1" with quantity 2
        Then the cart should contain 1 item
        And the cart total should be 20.00

    Scenario: Remove item from cart
        Given I have added product "PROD1" with quantity 2
        When I remove product "PROD1" from the cart
        Then the cart should be empty

    Scenario Outline: Add multiple items to cart
        When I add product "<product_id>" with quantity <quantity>
        Then the cart should contain 1 item
        And the cart total should be <expected_total>

        Examples:
            | product_id | quantity | expected_total |
            | PROD1     | 1        | 10.00         |
            | PROD2     | 2        | 40.00         |
            | PROD3     | 3        | 90.00         |

    Scenario: Update item quantity
        Given I have added product "PROD1" with quantity 1
        When I update the quantity of product "PROD1" to 3
        Then the cart should contain 1 item
        And the cart total should be 30.00