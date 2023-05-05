Friday May 5 end of sprint 1

# For Friday:
## Progress so far:
    - The start of all users stories have been added, these being:
        - Non-logged in users
        - Logged in users
        - Admin Users
    - Current users are/user stories: 
        - Admin
            - username: admin
            - password: password
        - User
            - username: username
            - password: password
        - Non-logged in users
            - none
    - These users have different permissions 
        - Admin can view the /admin/store
        - User can view the /store
        - Non-logged in users can view the /info
    ## Presentation  
        1. `/` => show the front page
        2. `/info` => show the info page
        3. `/store` => show the store
            - user will be redirected to login as they are not logged in
        4. `/admin/store` => show the admin store
            - user will be redirected to login as they are not admin
        5. `/login` => show the login page => click **sign up** button
        6. `/createaccount` => show the create account and create a new account
        7. `/store` => show the store as logged in user
        8. click **log out**
        9. `/admin` => sign in as admin
        10. `/admin/store` => show that the admin store front/auth works