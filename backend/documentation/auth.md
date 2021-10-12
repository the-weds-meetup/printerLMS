# Authentication Module Documentation

> Authentication methods to ensure identity of user

## Login

> POST: /api/auth/login

Token should be used to be saved on the user LocalStorage upon login.
To authenticate the idenity of the user when they use any in-app function
whenever possible

### Requires

```js
{
  email: String,
  password: String,
}
```

### Returns

```js
// Success
{
  success: True, // boolean
  result: {
    type: "Login", // string
    records: [
      {
        token: "XXXXX-XXXXX-XXXXX-XXXXX", // string
        expiry_date: "2020-1-01T00:00:00.0000Z", // string
      }
    ]
  }
}


// Failure
{
  success: False, // boolean
  result: {
    type: "Login", // string
    message: "An error has occured" // string
  }
}
```

## Logout

> POST: /api/auth/logout

Updates the session token

### Requires

```js
{
  token: String,
}
```

### Returns

```js
// Success
{
  success: True, // boolean
  result: {
    type: "Logout", // string
    message: "Success" // string
  }
}


// Failure
{
  success: False, // boolean
  result: {
    type: "Logout", // string
    message: "Invalid token"  // string
  }
}
```

## ValidateToken

> No url avaiable

Validates if token is expired or not.

Use the function to check if the session is authentic, before proceeding with the feature the user wants

### Requires

```js
{
  token: String,
}
```

### Returns

```js
// Success || Failure
{
  status: Boolean,
  message: String,
}
```
