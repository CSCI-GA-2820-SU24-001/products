Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
<<<<<<< HEAD
        | name    | description        | price | available | category |
        | Pen     | Blue ink pen       | 1.20  | True      | STATIONERY |
        | Notebook| Spiral notebook    | 2.50  | False     | STATIONERY |
        | Apple   | Fresh red apple    | 0.99  | True      | FOOD      |
        | Mug     | Ceramic coffee mug | 5.00  | True      | KITCHEN   |
=======
        | name       | description     | price   | available | category   |
        | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
        | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
        | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
        | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |
>>>>>>> set-environment

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Catalog Administration" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
<<<<<<< HEAD
    And I set the "Name" to "Bottle"
    And I set the "Description" to "Water bottle"
    And I select "True" in the "Available" dropdown
    And I select "KITCHEN" in the "Category" dropdown
    And I set the "Price" to "3.75"
=======
    And I set the "Name" to "Hammer"
    And I set the "Description" to "Claw hammer"
    And I select "True" in the "Available" dropdown
    And I select "Tools" in the "Category" dropdown
    And I set the "Price" to "34.95"
>>>>>>> set-environment
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
<<<<<<< HEAD
    And I should see "Bottle" in the "Name" field
    And I should see "Water bottle" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "KITCHEN" in the "Category" dropdown
    And I should see "3.75" in the "Price" field
=======
    And I should see "Hammer" in the "Name" field
    And I should see "Claw hammer" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "Tools" in the "Category" dropdown
    And I should see "34.95" in the "Price" field
>>>>>>> set-environment
