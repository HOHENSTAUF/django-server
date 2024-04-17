# django-server
=======
**Simple REST API using Django REST Framework**

Authentication uses token-based model.
Tokens are generated with PyJWT. *Refresh Token* is stored in database along with user information,
*Access Token* could be retrieved via login or refresh requests, using *Refresh Token*. I've also choose to use JWT to encode 
*user id* and *expiration time* of the *Refresh Token*. 
There is a lot of work to be done to make the API truly safe and functional, however, on this particular stage
I focused on realisation of each given objective which are:

- RESTful API must be developed with Django and Django REST Framework.
- Access Token is not stored in the database; it’s verified in authentication endpoints without database calls, using the PyJWT library.
- Refresh Token should be stored in the database with its expiry time and linked to a user.
- Use the django-constance module for managing the lifetimes of Access and Refresh tokens.
- API Documentation: Provide a browsable API with endpoint documentation.
  
and now it all works.

Endpoints are provided to:
- Register user
- Login user
- Refresh user's access token
- Logout user (deleting his refresh token from database)
- Retrieve personal information using access token
- Update personal information using access token
