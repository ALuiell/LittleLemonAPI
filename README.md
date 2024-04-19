
Little Lemon Restaurant API Project
Introduction
This project involves creating a fully functional API for the Little Lemon restaurant, facilitating the development of web and mobile applications by client application developers. It enables users with different roles to perform various tasks such as browsing, adding, and editing menu items, placing orders, browsing orders, assigning delivery crew to orders, and delivering orders.

Scope
The API project includes endpoints for managing users, menu items, user groups, cart items, and orders. Users with different roles, including administrators, managers, delivery crew, and customers, have access to different functionalities based on their roles and permissions.

User Registration and Token Generation Endpoints

Create User
Endpoint: POST /api/users
Role: No role required
Method: POST
Purpose: Creates a new user with name, email, and password.

Get Current User
Endpoint: GET /api/users/me/
Role: Anyone with a valid user token
Method: GET
Purpose: Displays information about the current user.

Generate Token
Endpoint: POST /token/login/
Role: Anyone with a valid username and password
Method: POST
Purpose: Generates access tokens for authentication.

Menu Items Endpoints
These endpoints handle the management of menu items, allowing customers, delivery crew, and managers to perform various actions such as listing, adding, updating, and deleting menu items.

List All Menu Items
Endpoint: GET /api/menu-items
Role: Customer, delivery crew
Method: GET
Purpose: Lists all menu items. Returns a 200 – Ok HTTP status code.

Manage Menu Items
Endpoint: POST /api/menu-items, PUT /api/menu-items/{menuItem}, PATCH /api/menu-items/{menuItem}, DELETE /api/menu-items/{menuItem}
Role: Customer, delivery crew
Method: POST, PUT, PATCH, DELETE
Purpose: Denies access and returns 403 – Unauthorized HTTP status code for unauthorized users.

Get Single Menu Item
Endpoint: GET /api/menu-items/{menuItem}
Role: Customer, delivery crew
Method: GET
Purpose: Lists details of a single menu item.

Manage Menu Items (Manager)
Endpoint: GET /api/menu-items, POST /api/menu-items, PUT /api/menu-items/{menuItem}, PATCH /api/menu-items/{menuItem}, DELETE /api/menu-items/{menuItem}
Role: Manager
Purpose: Allows managers to list, create, update, and delete menu items.

These endpoints facilitate the management of menu items in the system, ensuring smooth operation and accessibility for all users based on their roles and permissions.

User Group Management Endpoints
These endpoints manage user groups within the system, allowing managers to assign users to specific groups and remove them as needed.

List Managers
Endpoint: GET /api/groups/manager/users
Role: Manager
Method: GET
Purpose: Returns a list of all managers.

Assign User to Manager Group
Endpoint: POST /api/groups/manager/users
Role: Manager
Method: POST
Purpose: Assigns the user specified in the payload to the manager group. Returns 201 - Created.

Remove User from Manager Group
Endpoint: DELETE /api/groups/manager/users/{userId}
Role: Manager
Method: DELETE
Purpose: Removes the specified user from the manager group. Returns 200 - Success if everything is okay. If the user is not found, returns 404 - Not found.

List Delivery Crew
Endpoint: GET /api/groups/delivery-crew/users
Role: Manager
Method: GET
Purpose: Returns a list of all delivery crew members.

Assign User to Delivery Crew Group
Endpoint: POST /api/groups/delivery-crew/users
Role: Manager
Method: POST
Purpose: Assigns the user specified in the payload to the delivery crew group. Returns 201 - Created.

Remove User from Delivery Crew Group
Endpoint: DELETE /api/groups/delivery-crew/users/{userId}
Role: Manager
Method: DELETE
Purpose: Removes the specified user from the delivery crew group. Returns 200 - Success if everything is okay. If the user is not found, returns 404 - Not found.

Cart Management Endpoints
These endpoints handle the management of the user's shopping cart, allowing customers to view, add, and remove items from their cart.

View Cart Items
Endpoint: GET /api/cart/menu-items
Role: Customer
Method: GET
Purpose: Returns the current items in the cart for the authenticated user.

Add Item to Cart
Endpoint: POST /api/cart/menu-items
Role: Customer
Method: POST
Purpose: Adds the specified menu item to the cart. Sets the authenticated user as the owner of these cart items.

Remove All Items from Cart
Endpoint: DELETE /api/cart/menu-items
Role: Customer
Method: DELETE
Purpose: Deletes all menu items from the cart for the current user.

These endpoints facilitate the management of the user's shopping cart, providing essential functionality for browsing, adding, and removing items during the shopping experience.

Order Management Endpoints
These endpoints manage the creation, retrieval, and update of orders within the system, allowing customers, managers, and delivery crew to perform various actions related to orders.

List Orders (Customer)
Endpoint: GET /api/orders
Role: Customer
Method: GET
Purpose: Returns all orders with order items created by the current user.

Create Order (Customer)
Endpoint: POST /api/orders
Role: Customer
Method: POST
Purpose: Creates a new order item for the current user. Retrieves current cart items and adds them to the order items table. Deletes all items from the cart for this user.

View Order Details (Customer)
Endpoint: GET /api/orders/{orderId}
Role: Customer
Method: GET
Purpose: Returns all items for the specified order id. Displays an appropriate HTTP error status code if the order ID doesn’t belong to the current user.

List Orders (Manager)
Endpoint: GET /api/orders
Role: Manager
Method: GET
Purpose: Returns all orders with order items for all users.

Update Order (Manager)
Endpoint: PUT, PATCH /api/orders/{orderId}
Role: Manager
Method: PUT, PATCH
Purpose: Updates the order. A manager can set a delivery crew to this order and update the order status. If a delivery crew is assigned and the status is set to 0, it means the order is out for delivery. If the status is set to 1, it means the order has been delivered.

Delete Order (Manager)
Endpoint: DELETE /api/orders/{orderId}
Role: Manager
Method: DELETE
Purpose: Deletes the specified order.

List Orders (Delivery Crew)
Endpoint: GET /api/orders
Role: Delivery crew
Method: GET
Purpose: Returns all orders with order items assigned to the delivery crew.

Update Order Status (Delivery Crew)
Endpoint: PATCH /api/orders/{orderId}
Role: Delivery crew
Method: PATCH
Purpose: Updates the order status to 0 or 1. The delivery crew can only update the order status and nothing else in this order.

These endpoints provide comprehensive functionality for managing orders within the system, catering to the needs of customers, managers, and delivery crew.

