# FastAPI-Modular-Boilerplate

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![GitHub stars](https://img.shields.io/github/stars/ihor-vt/FastAPI-Modular-Boilerplate.svg)](https://github.com/yourusername/FastAPI-Modular-Boilerplate/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ihor-vt/FastAPI-Modular-Boilerplate.svg)](https://github.com/yourusername/FastAPI-Modular-Boilerplate/network)
[![GitHub issues](https://img.shields.io/github/issues/ihor-vt/FastAPI-Modular-Boilerplate.svg)](https://github.com/yourusername/FastAPI-Modular-Boilerplate/issues)
[![GitHub license](https://img.shields.io/github/license/ihor-vt/FastAPI-Modular-Boilerplate.svg)](https://github.com/yourusername/FastAPI-Modular-Boilerplate/blob/main/LICENSE)

FastAPI-Modular-Boilerplate is a powerful starter template for developing scalable web applications using FastAPI. Inspired by Django's best practices, this template offers a modular structure that ensures clear code organization and easy functionality expansion.

## 🚀 Features

- 📁 Modular project structure
- 🔒 Built-in authentication and authorization system
- 📊 Preconfigured database connection using SQLAlchemy
- 🐳 Docker support for easy deployment
- 🧪 Ready-to-use testing structure
- 📝 Automatic API documentation generation

## 🛠️ Quick Start

1. Clone the repository:

   ```
   git clone https://github.com/ihor-vt/FastAPI-Modular-Boilerplate.git
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables in the `.env` file

5. Run migrations:

   ```
   alembic upgrade head
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

## 📖 Project Structure

```
my_fastapi_project/
│
├── manage.py
├── config/
│   ├── settings.py
│   ├── database.py
│   └── main.py
│
├── apps/
│   ├── users/
│   ├── auth/
│   └── common/
│
├── migrations/
├── tests/
├── static/
└── templates/
```

## 🤝 How to Contribute

We always welcome new contributors! If you want to contribute to the project, please:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes and commit them (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- The FastAPI team for the excellent framework
- The developer community for inspiration and support

---

Let's make FastAPI even better together! 🚀✨
