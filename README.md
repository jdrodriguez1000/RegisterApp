# RegisterApp

A secure, multi-platform user registration system built with **Flet** and the **Fleting** micro-framework, using **Supabase** for authentication and data persistence.

## 🚀 Features

- **Multi-platform**: Runs on Web, Mobile, and Desktop from a single Python codebase.
- **Secure Authentication**: Integrated with Supabase Auth (Registration, Login, Password Recovery).
- **Mobile-First Design**: Responsive UI optimized for mobile devices.
- **Internationalization**: Support for Spanish and English.
- **Admin Panel**: Dashboard for user management and metrics.

## 🏗️ Architecture

The project follows the **MVC (Model-View-Controller)** pattern provided by the **Fleting** framework.

- `core/`: Framework infrastructure.
- `configs/`: App settings and route definitions.
- `views/`: UI components and layouts.
- `controllers/`: Business logic.
- `models/`: Data structures.

## 🛠️ Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/USERNAME/RegisterApp.git
   cd RegisterApp
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   python main.py
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
