# Freelance Marketplace Django

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
  - [Database Configuration](#database-configuration)
  - [Razorpay Integration](#razorpay-integration)
  - [Static and Media Files](#static-and-media-files)
  - [Additional Configuration](#additional-configuration)
- [Migrations](#migrations)
- [Usage](#usage)
- [Contributing](#contributing)
- [Testing](#testing)
- [License](#license)
- [Contact](#contact)


## Overview

Freelance Marketplace Django is a powerful platform built on Django, facilitating seamless interactions between freelancers and clients. It provides a comprehensive solution for freelance service exchanges with a focus on security, efficiency, and ease of use.

## Features

- **User Authentication**: Secure sign-up and login functionalities with password hashing and JWT tokens.
- **Service Management**: Easy-to-use interface for freelancers to list, edit, and manage their services, including pricing and descriptions.
- **Order Processing**: Smooth order management system with real-time updates on order status.
- **Real-time Chat**: Built-in chat functionality for direct communication between freelancers and clients.
- **Payment Integration**: Secure payment gateway integration for hassle-free transactions.
- **Search and Filter**: Efficient search and filter options for finding relevant services.
- **Admin Panel**: Admin dashboard for managing users, services, orders, and site settings.

## Technology Stack

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL (production) 
- **Others**: Celery for asynchronous task processing, Redis for caching, Bootstrap 5 for frontend styling

### Razorpay Integration

This project utilizes Razorpay for payment gateway integration. Razorpay is a leading payment gateway provider in India, offering secure and seamless payment processing solutions.

### Bootstrap 5

Bootstrap 5 is used for frontend styling and layout. It provides a comprehensive set of responsive design components and utilities, making it easier to build modern and mobile-friendly web interfaces.


## Installation

### Prerequisites

Before getting started, ensure you have the following prerequisites installed on your system:

- Python 3.8+
- pip (Python package installer)
- PostgreSQL

```bash
git clone https://github.com/anfiquehussain/Freelance-Marketplace-Django.git
```

2. **Navigate to the project directory:**

```bash
cd Freelance-Marketplace-Django
```

3. **Create and activate a virtual environment:**

- On Windows:
  ```
  py -m venv env
  ```
  ```
  env\Scripts\activate
  ```
- On Unix or MacOS:
  ```
  python -m venv env
  ```
  ```
  source env/bin/activate
  ```

4. **Install dependencies:**
```
pip install -r requirements.txt
```

## Configuration
Before running the application, configure the environment variables as per your setup by creating a `.env` file in the project root with the necessary values.


### Database Configuration

In the `settings.py` file, configure the database settings according to your setup:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',  # Or your PostgreSQL server's address
        'PORT': '5432',       # Default PostgreSQL port
    }
}
```

#### Razorpay Integration
For Razorpay integration, provide your Razorpay publishable and secret keys:
```
REZORPAY_PUBLISHABLE_KEY = 'your_razorpay_publishable_key'
REZORPAY_SECRET_KEY = 'your_razorpay_secret_key'
```

### Static and Media Files
Configure the settings for static and media files:
```
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
```
Ensure that you have proper file permissions and directory structures set up for media file uploads.

### Additional Configuration
You may need to configure other settings based on your project's requirements, such as email configuration, security settings, and third-party API integration.


## Migrations

Before running the application, you need to apply the migrations to set up the database schema. Follow these steps:

1. **Navigate to the project directory:**

    ```bash
    cd Freelance-Marketplace-Django
    ```

2. **Activate the virtual environment (if not already activated):**

    - On Windows:
      ```bash
      env\Scripts\activate
      ```
    - On Unix or MacOS:
      ```bash
      source env/bin/activate
      ```

3. **Check for Missing Migrations (Optional):**

    It's a good practice to check if there are any new migrations that need to be created. Run the following command to generate new migrations based on model changes:

    ```bash
    python manage.py makemigrations
    ```

    This command will inspect the models and create new migration files if any changes are detected. Review the changes and migrate them if necessary.

4. **Apply Migrations:**

    Run the following command to apply migrations:

    ```bash
    python manage.py migrate
    ```

    This command will create the necessary tables in the database based on the models defined in the Django app.

5. **Create Superuser (Optional):**

    If you want to access the Django admin interface, you can create a superuser using the following command:

    ```bash
    python manage.py createsuperuser
    ```

    Follow the prompts to create a superuser account.

Now, your database schema is set up, and you're ready to run the application.



## Usage
To run the development server:

```
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to access the application.


## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with meaningful commit messages.
4. Push your branch and open a pull request.


## Testing
### Running Tests
To run tests for the project, use the following command:
```
python manage.py test
```

This command will execute all the test cases defined in the project and provide feedback on their success or failure.

Testing Framework
The project uses the Django testing framework for unit tests, integration tests, and functional tests. It provides a comprehensive set of tools for writing and running tests to ensure


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.


## Contact
For any queries or further assistance, please contact [Anfique Hussain V](mailto:anfiquehussain6@gmail.com).
<p align="left">
<a href="https://dev.to/anfiquehussain" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/devto.svg" alt="anfiquehussain" height="30" width="40" /></a>
<a href="https://twitter.com/anfique_hv" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg" alt="anfique_hv" height="30" width="40" /></a>
<a href="https://linkedin.com/in/anfique-hussain-v-aa8841290" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="anfique-hussain-v-aa8841290" height="30" width="40" /></a>
<a href="https://stackoverflow.com/users/16822116" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/stack-overflow.svg" alt="16822116" height="30" width="40" /></a>
<a href="https://fb.com/100022489001636" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/facebook.svg" alt="100022489001636" height="30" width="40" /></a>
<a href="https://instagram.com/anfique_hv" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="anfique_hv" height="30" width="40" /></a>
<a href="https://www.hackerearth.com/@anfiquehussain1" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/hackerearth.svg" alt="@anfiquehussain1" height="30" width="40" /></a>
</p>
