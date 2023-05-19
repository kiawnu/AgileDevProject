# For Friday:
## Deliverables:
    - Create logic using flask to add functionality to store system. Where customers can affect the inventory values 
    - Customers must be able to cancel order, create order, and change order before purchase      


## Presentation 
1. 

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



    order = db.session.get(Order, order_id)
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M")

    for product_order in order.products:
        product_obj = db.session.get(Product, product_order.product_name)
        if (product_obj.quantity - product_order.quantity) < 0:
            product_order.quantity = product_obj.quantity
            product_obj.quantity = 0
        else:
            product_obj.quantity -= product_order.quantity

        db.session.add(product_obj)
        db.session.commit()
    order.date_processed = date
    order.completed = True
    db.session.add(order)

    db.session.commit()

    return api_get_order(order_id)