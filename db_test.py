from app import app, db
from models import User, Content

try:
    # Inserting data into the database
    with app.app_context():
        # Create a new user
        user = User(username='john0', password='password123', role='admin')
        db.session.add(user)
        db.session.commit()

        print('User ID:', user.id)

        # Create a new content associated with the user
        content = Content(title='Sample Content', body='This is a test content.', user=user)
        db.session.add(content)
        db.session.commit()

        print('Content ID:', content.id)
        print('Content Title:', content.title)
        print('Content Body:', content.body)

    # Querying data from the database
    with app.app_context():
        # Get all users
        users = User.query.all()
        for user in users:
            print(f"User {user.id}: {user.username}")

        # Get a specific user by ID
        user = db.session.get(User, 2)
        print(user.username)

        # Get all contents associated with a specific user
        contents = user.contents
        for content in contents:
            print(content.title)

    # Updating data in the database
    with app.app_context():
        # Get a specific user by ID
        user = db.session.get(User, 2)

        print(user.password)

        # Update the user's password
        user.password = 'newpassword'
        db.session.commit()

        print(user.password)

    with app.app_context():
        # Get a specific user by ID
        user = db.session.get(User, 1)

        if user:
            # Delete the user's contents
            Content.query.filter_by(userId=user.id).delete()
            db.session.commit()

            # Delete the user
            db.session.delete(user)
            db.session.commit()

            print("User and associated contents deleted successfully.")
        else:
            print("User not found.")


    # DELETES ALL DATA FROM THE DATABASE
    # with app.app_context():
    #     # Delete all users
    #     User.query.delete()
    #     db.session.commit()

    #     # Delete all contents
    #     Content.query.delete()
    #     db.session.commit()

    #     print("All data deleted successfully.")

except Exception as e:
    print("An error occurred:", str(e))
