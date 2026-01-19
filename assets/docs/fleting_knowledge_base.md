# Fleting & Flet Technical Knowledge Base

This document serves as a comprehensive guide for building applications using the **Flet** motor and the **Fleting** micro-framework architecture.

## 🚀 Overview

- **Flet**: A framework to build interactive multi-platform apps in Python using Flutter for rendering.
- **Fleting**: An opinionated micro-framework that adds structure, MVC patterns, and productivity tools on top of Flet.

---

## 🧱 Project Structure (Fleting)

A standard Fleting project follows this hierarchy:

```text
project_root/
├── core/               # Framework infrastructure (App, Router, State, etc.)
├── configs/            # Global configurations
│   ├── app_config.py   # General app settings
│   ├── routes.py       # Route mapping (lazy loading)
│   └── languages/      # i18n JSON files (es.json, pt.json)
├── views/
│   ├── layouts/        # Reusable layouts (AppBar, SideBar, etc.)
│   └── pages/          # Individual page views
├── controllers/        # Logic handlers
├── models/             # Data structures
├── cli/                # Project management CLI
├── main.py             # Entry point
└── runtime_imports.py  # Imports for Windows builds
```

---

## 🛠️ Core Directory Breakdown

These files form the heart of a Fleting project, managing infrastructure and global services:

- **`core/app.py`**: The main orchestrator. It configures the Flet application, initializes the state, sets up window resize listeners, and builds the dynamic UI components (like the AppBar) according to the current language.
- **`core/state.py`**: Manages the global `AppState`. It stores critical runtime information such as the current `device` type, active `language`, and navigation status.
- **`core/router.py`**: Handles all navigation logic. It looks up routes in `configs/routes.py`, manages view transitions, and handles "Page Not Found" errors.
- **`core/responsive.py`**: Contains the logic to determine the device type (`mobile`, `tablet`, or `desktop`) based on window width, enabling the "Mobile-First" approach.
- **`core/i18n.py`**: Directs the internationalization system. It loads translation files from `configs/languages/` and provides the `I18n.t()` helper for localized strings.
- **`core/database.py`**: Centralizes database connections. It often implements a singleton pattern to provide a shared connection across the app (supports SQLite and MySQL out of the box).
- **`core/logger.py`**: Provides a unified logging interface that works across development and production (Android/Executables), writing to both console and `fleting.log`.
- **`core/error_handler.py`**: A global exception catcher that prevents application crashes by showing a user-friendly error screen and logging the stacktrace.

---

## 🧭 Architecture

### View Rendering Flow
Fleting decouples content from layout:
1. **View (Pure Content)**: Defines what is shown.
2. **Layout (Structure)**: Wraps the view with persistent UI elements (AppBars, etc.).
3. **Page (Flet)**: The root container.

### Simple View Implementation Example:
```python
class HomeView:
    def render(self):
        content = ft.Text("Welcome to the Home Page")
        # Return the content wrapped in a layout
        return MainLayout(page, content, router)
```

---

## 🛠️ Key Native Features

### 1. Responsiveness
Managed via `AppState.device`. values: `mobile`, `tablet`, or `desktop`.
- Automatically updates on window resize.
- Access via: `from core.state import AppState`

### 2. Internationalization (i18n)
- Configured in `configs/languages/`.
- Usage: `I18n.t("key.subkey")`.

### 3. Routing
- Defined in `configs/routes.py`.
- Supports lazy loading: `ROUTE_MAP = {"/": "views.pages.home_view.HomeView"}`.

### 4. CLI (Command Line Interface)
Fleting includes a CLI to scaffold components:
- `python fleting.py create:page Name`
- `python fleting.py create:layout Name`

---

## 🤖 Guidance for AI Agents

When building a project with this stack, follow these rules:

1. **MVC Adherence**: Keep logic in `controllers/`, data in `models/`, and UI in `views/`.
2. **Lazy Routing**: Always register new pages in `configs/routes.py`.
3. **Mobile-First**: Design for `mobile` and use `AppState.device` to scale up to `desktop`.
4. **i18n by Default**: Never hardcode strings in the UI. Use `I18n.t()`.
5. **Layouts**: Use the `layouts/` directory to share common UI structures across pages.
6. **Logging**: Utilize `core.logger` for consistent debugging.

---

## 📚 Reference Links
- [Fleting GitHub](https://github.com/alexyucra/Fleting)
- [Official Flet Docs](https://flet.dev/docs/)
