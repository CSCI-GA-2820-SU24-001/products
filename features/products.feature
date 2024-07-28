Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name    | description        | price | available | category |
        | Pen     | Blue ink pen       | 1.20  | True      | STATIONERY |
        | Notebook| Spiral notebook    | 2.50  | False     | STATIONERY |
        | Apple   | Fresh red apple    | 0.99  | True      | FOOD      |
        | Mug     | Ceramic coffee mug | 5.00  | True      | KITCHEN   |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Catalog Administration" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Bottle"
    And I set the "Description" to "Water bottle"
    And I select "True" in the "Available" dropdown
    And I select "KITCHEN" in the "Category" dropdown
    And I set the "Price" to "3.75"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Bottle" in the "Name" field
    And I should see "Water bottle" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "KITCHEN" in the "Category" dropdown
    And I should see "3.75" in the "Price" field