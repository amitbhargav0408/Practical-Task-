# Practical-Task-
Practical Task  Create a Django/Flask application 
#Questions
Practical Task

Create a Django/Flask application
Create login and registration routes
Registration should be done using these fields 
Email
Password
Name
User can login using email and password
Once logged in user will get JWT Token which will be valid only for 5 hours
Create a protected route products
User can list all products after login only
User can also filter the products by search query (on title and description)
User can filter using price (min, max)
User can add a new product
Product fields
Title
description
Images (multiple)
Price
Discount

#Testing-1 Create login and registration routes

curl --header "Content-Type: application/json" \
>      --request POST \
>      --data '{"email":"amitbhargav134@gmail.com","password":"password123","name":"Amit bhargav"}' \
>         http://localhost:5000/register"""

#Testing-2 User can login using email and password

curl --header "Content-Type: application/json"  --request POST   --data '{"email":"amitbhargav134@gmail.com","password":"password123"}'  \  http://localhost:5000/login

#User can also filter the products by search query (on title and description) & User can filter using price (min, max)
curl --header "Content-Type: application/json" \
     --header "Authorization: Bearer <JWT_TOKEN>" \
     --request GET \
        "http://localhost:5000/products?search=book&min_price=30.99&max_price=10.99"
     
#User can add a new product
curl --header "Content-Type: application/json" \ 
           --header "Authorization: Bearer         eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NjM3NzI2NCwianRpIjoiNWEwODNhMDQtMGMzZS00MGVjLTg3ZGItZmRjMjI4MWQ0MjliIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImpvaG5AZXhhbXBsZS5jb20iLCJuYmYiOjE2NzYzNzcyNjQsImV4cCI6MTY3NjM5NTI2NH0.mvdaVmQoxZvvOkECrJbBFkwxr5ptAZe1a5PZA3QkeRw"     \
    --request POST --data '{"title":"phonr","description":"phone description.","images":"test.jpg","price":30.99,"discount":0.3}'                     http://localhost:5000/products
    
    

    --data '{"title":"phonr","description":"phone description.","images":"test.jpg","price":30.99,"discount":0.3}'
