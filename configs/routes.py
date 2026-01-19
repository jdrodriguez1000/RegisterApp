
import flet as ft
import importlib

ROUTES = [
    {
        "path": "/",
        "view": "views.pages.welcome_view.WelcomeView",
        "label": "welcome.title",
        "icon": ft.Icons.START,
        "show_in_top": False,
        "show_in_bottom": False,
    },
    {
        "path": "/login",
        "view": "views.pages.login_view.LoginView",
        "label": "login.title",
        "icon": ft.Icons.LOGIN,
        "show_in_top": False,
        "show_in_bottom": False,
    },
    {
        "path": "/construction",
        "view": "views.pages.under_construction_view.UnderConstructionView",
        "label": "construction.title",
        "icon": ft.Icons.CONSTRUCTION,
        "show_in_top": False,
        "show_in_bottom": False,
    },
    {
        "path": "/register",
        "view": "views.pages.register_view.RegisterView",
        "label": "register.title",
        "icon": ft.Icons.APP_REGISTRATION,
        "show_in_top": False,
        "show_in_bottom": False,
    },
    {
        "path": "/verification-pending",
        "view": "views.pages.email_verification_pending_view.EmailVerificationPendingView",
        "label": "verification.title",
        "icon": ft.Icons.VERIFIED_USER,
        "show_in_top": False,
        "show_in_bottom": False,
    },
    {
        "path": "/profile-completion",
        "view": "views.pages.profile_completion_view.ProfileCompletionView",
        "label": "Completar Perfil",
        "icon": ft.Icons.PERSON,
        "show_in_top": False,
        "show_in_bottom": False,
    },
    {
        "path": "/dashboard",
        "view": "views.pages.dashboard_view.DashboardView",
        "label": "menu.home",
        "icon": ft.Icons.DASHBOARD,
        "show_in_top": True,
        "show_in_bottom": False,
    },
    {
        "path": "/settings",
        "view": "views.pages.settings_view.SettingsView",
        "label": "menu.settings",
        "icon": ft.Icons.SETTINGS,
        "show_in_top": True,
        "show_in_bottom": False,
    },
    {
        "path": "/help",
        "view": "views.pages.help_view.HelpView",
        "label": "menu.help",
        "icon": ft.Icons.HELP,
        "show_in_top": True,
        "show_in_bottom": False,
    }
]

def load_view(view_path: str):
    module_name, class_name = view_path.rsplit(".", 1)
    
    try:
        module = importlib.import_module(module_name)
        view_class = getattr(module, class_name)
        return view_class
    except (ImportError, AttributeError) as e:
        print(f"Erro ao carregar view {view_path}: {e}")
        return None

def get_routes():
    routes = {}

    for r in ROUTES:
        def create_view_lambda(path=r["view"]):
            return lambda page, router: load_view(path)(page, router).render()

        routes[r["path"]] = create_view_lambda()

    return routes

routes = get_routes()

