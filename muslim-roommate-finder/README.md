# Muslim Roommate Finder

A Django web application designed to help Muslims find compatible roommates who share similar values, lifestyle preferences, and religious practices.

## Features

- **User Authentication**: Secure registration and login system
- **Profile Management**: Create and manage detailed user profiles
- **Room Listings**: Post and browse available rooms with detailed information
- **Advanced Search**: Filter rooms by location, amenities, price, and preferences
- **Messaging System**: Direct communication between users
- **Admin Interface**: Comprehensive admin panel for content management
- **Responsive Design**: Modern, mobile-friendly user interface

## Technology Stack

- **Backend**: Django 4.2+ with Python 3.8+
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Render.com ready

## Project Structure

```
muslim-roommate-finder/
├── config/                 # Django project settings
├── core/                   # Main application
│   ├── admin/             # Admin interface configurations
│   ├── management/        # Custom Django commands
│   ├── migrations/        # Database migrations
│   └── models.py          # Database models
├── static/                # Static files (CSS, JS, images)
├── templates/             # HTML templates
├── media/                 # User uploaded files
└── requirements.txt       # Python dependencies
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd muslim-roommate-finder
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   python manage.py loaddata core/fixtures/initial_data.json
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Usage

1. **Access the application** at `http://127.0.0.1:8000/`
2. **Register** a new account or login with existing credentials
3. **Create a profile** with your preferences and requirements
4. **Browse rooms** or create your own room listing
5. **Contact other users** through the messaging system

## Key Models

- **User**: Extended Django user model with additional fields
- **Profile**: User profile with preferences and contact information
- **Room**: Room listings with details, amenities, and images
- **Message**: Communication between users
- **Review**: User reviews and ratings

## Deployment

The application is configured for deployment on Render.com:

1. Connect your GitHub repository to Render
2. Set environment variables in Render dashboard
3. Deploy using the included `render.yaml` configuration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@muslimroommatefinder.com or create an issue in the repository.
