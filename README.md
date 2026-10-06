# Qt Application Skeleton

> ⚠️ **Work in progress.**
> This repository provides a reusable skeleton for building cross-platform desktop applications with Python and Qt using **PySide6** and the **Model-View-Controller (MVC)** pattern.

The project is designed to provide a clean and maintainable foundation for applications that may grow to include multiple independent features and integrations with external REST APIs.

## Table of contents

* [Project goal](#project-goal)
* [Architecture](#architecture)
* [Repository structure](#repository-structure)
* [Technologies](#technologies)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Building the application](#building-the-application)
* [Localization](#localization)
* [Application themes](#application-themes)
* [Adding a new feature](#adding-a-new-feature)
* [External API integrations](#external-api-integrations)
* [Testing](#testing)
* [Continuous integration](#continuous-integration)
* [Design principles](#design-principles)
* [Project status / roadmap](#project-status--roadmap)
* [License](#license)

## Project goal

The purpose of this project is to provide a reusable starting point for developing cross-platform applications with Python and Qt.

The skeleton provides:

* A structured **MVC architecture**.
* A permanent main application window with navigation controls.
* Internal navigation using `QStackedWidget`.
* Centralized application lifecycle management.
* Independent Models, Views and Controllers for each feature (`Home`, `Logs`, `Settings`, `Route Designer`, `Video Uploader`).
* Custom Qt widgets (`CheckableComboBox`, `SpeedometerProgress`).
* A generic core layer for infrastructure shared by the application (logging, configuration, text binding, main window).
* A provider layer for external service integrations with a generic HTTP client (`HttpClient`).
* Qt-based HTTP communication through `QNetworkAccessManager`.
* Localization support using Qt `.ts` and `.qm` translation files (`en_US`, `es_ES`).
* Cross-platform build scripts (`build.sh`, `build.ps1`) and PyInstaller support for creating distributable applications.
* A predictable structure for adding new features.

The skeleton itself is intentionally kept independent from any particular business domain.

## Architecture

The application follows the **Model-View-Controller (MVC)** pattern.

```text
                    Application
                         │
                         ▼
                    MainWindow
                         │
                         ▼
                    Navigation
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
            View               Controller
                                    │
                                    ▼
                                  Model
                                    │
                                    ▼
                                 Provider
                                    │
                                    ▼
                              HTTP / REST API
```

### Application

`Application` is responsible for the application lifecycle and for composing the main application components.

It owns the lifetime of Models, Views and Controllers.

The application entry point (`main.py`) should remain intentionally small.

### MainWindow

`MainWindow` is the permanent Qt application window.

It is responsible for:

* Window configuration.
* The central application widget.
* Hosting the application's navigation container and sidebar/toolbar.

The main window remains alive while the user navigates between different features.

### View

Views contain the graphical user interface.

A View is responsible for:

* Creating Qt widgets and custom widgets (e.g., `CheckableComboBox`, `SpeedometerProgress`).
* Displaying information.
* Emitting UI events.
* Updating its own visual state.

Views must not contain business logic.

### Controller

Controllers coordinate communication between Views and Models.

A Controller is responsible for:

* Receiving UI events from the View.
* Calling the appropriate Model methods.
* Processing Model results when necessary.
* Updating the View.

Controllers must not contain GUI implementation details or business logic that belongs to the Model.

### Model

Models contain application and business logic.

A Model is responsible for:

* Application logic.
* Data processing and logging.
* Calculations.
* Validation.
* Communication with providers when appropriate.

Models must not manipulate Qt widgets directly.

### Provider

Providers isolate integrations with external services.

For example:

```text
providers/
└── http/
    └── http_client.py

```

Each provider contains the implementation required to communicate with its corresponding external service or HTTP infrastructure.

Provider-specific logic must not leak into the generic application infrastructure.

### Core

The `core` package contains infrastructure shared by the application.

Examples include:

* Application lifecycle (`application.py`).
* Configuration management (`config.py`).
* Logging infrastructure (`logging.py`).
* Main window and navigation (`main_window.py`).
* Text binding utilities (`text_binder.py`).

The core layer must remain generic and must not contain provider-specific business logic.

## Repository structure

```text
.
├── main.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── skeleton_qt.spec
├── build.sh
├── build.ps1
│
├── resources/
│   ├── assets/
│   │   └── icon.ico
│   ├── styles/
│   │   ├── light.qss
│   │   └── dark.qss
│   └── translations/
│       ├── skeleton_en_US.qm
│       ├── skeleton_en_US.ts
│       ├── skeleton_es_ES.qm
│       └── skeleton_es_ES.ts
│
├── src/
│   ├── __init__.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── controller.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── application.py
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── main_window.py
│   │   └── text_binder.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── home_model.py
│   │   ├── logs_model.py
│   │   ├── model.py
│   │   ├── route_designer_model.py
│   │   ├── settings_model.py
│   │   └── video_uploader_model.py
│   │
│   ├── providers/
│   │   ├── __init__.py
│   │   └── http/
│   │       ├── __init__.py
│   │       └── http_client.py
│   │
│   └── views/
│       ├── __init__.py
│       ├── base_view.py
│       ├── custom_widgets/
│       │   ├── __init__.py
│       │   ├── checkable_combobox.py
│       │   └── speedometer_progress.py
│       ├── home_view.py
│       ├── logs_view.py
│       ├── route_designer_view.py
│       ├── settings_view.py
│       ├── video_uploader_view.py
│       └── views.py
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_controller.py
    ├── test_logging.py
    ├── test_models.py
    ├── test_text_binder.py
    └── test_theme.py
```

## Technologies

### Python

The application is developed using Python 3.10+.

### PySide6

PySide6 provides the Qt bindings used for:

* Graphical user interfaces.
* Signals and slots.
* Application lifecycle.
* Networking.
* Custom widgets and layouts.

### Qt Networking

External REST APIs are accessed using Qt's networking infrastructure via `QNetworkAccessManager` implemented inside `src/providers/http/http_client.py`.

The project intentionally avoids coupling the application to provider-specific Python SDKs.

### PyInstaller

PyInstaller is used to package the application into distributable executables using `skeleton_qt.spec` and automated build scripts (`build.sh`, `build.ps1`).

## Requirements

* Python 3.10+
* pip
* PySide6
* PyInstaller

The exact supported Python versions may evolve as the project develops.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd skeleton_qt
```

Create a virtual environment.

### Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

Run the application from the project root:

```bash
python main.py
```

The application starts the main Qt window and loads the initial application view.

## Building the application

The project includes build scripts and a PyInstaller specification file:

* `skeleton_qt.spec`
* `build.sh` (Linux / macOS)
* `build.ps1` (Windows PowerShell)

Build the application with:

```bash
# Using build scripts
./build.sh        # Linux / macOS
.\build.ps1       # Windows

# Or directly with PyInstaller
pyinstaller --clean --noconfirm skeleton_qt.spec
```

The generated application will be placed in the `dist/` directory.

The PyInstaller configuration builds a windowed application (`console=False`).
UPX compression is disabled to avoid antivirus false positives.

## Localization

The application is designed to use Qt's translation system.

Translation source files use the `.ts` and compiled `.qm` formats:

```text
resources/translations/
├── skeleton_en_US.ts
├── skeleton_en_US.qm
├── skeleton_es_ES.ts
└── skeleton_es_ES.qm
```

User-visible strings should use Qt's translation mechanism:

```python
self.tr("Show welcome message")
```

The translation workflow is based on Qt tools such as:

```text
pyside6-lupdate
pyside6-lrelease
```

## Testing

Install the development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the test suite (a QApplication is provided automatically by pytest-qt):

```bash
pytest
```

On headless environments, use the offscreen Qt platform:

```bash
QT_QPA_PLATFORM=offscreen pytest
```

## Continuous integration

The repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`)
that runs Ruff linting and the pytest suite on Linux and Windows with
Python 3.10–3.12 on every push and pull request.

## Application themes

The application uses global Qt Style Sheets (QSS), so the light and dark themes
apply to existing and newly created views without per-view styling.

Theme files are located in `resources/styles/`:

* `light.qss`: default theme.
* `dark.qss`: dark theme.

`Application` loads and applies the selected stylesheet to `QApplication`.
The Settings view can switch themes at runtime. When packaging with PyInstaller, both QSS files are included by `skeleton_qt.spec`.

## Adding a new feature

New application features should follow the MVC structure.

For example, a feature called `testing` contains:

```text
src/
├── models/
│   └── testing_model.py
│
├── controllers/
│   └── controller.py
│
└── views/
    └── testing_view.py
```

### 1. Model

Create a model derived from the base `Model` class (`src/models/model.py`).

The model contains the application's logic for the feature.

### 2. View

Create a view derived from `BaseView` (`src/views/base_view.py`).

The view contains the graphical interface and emits signals for user actions. Custom widgets can be added under `src/views/custom_widgets/`.

### 3. Controller

The controller `Controller` (`src/controllers/controller.py`) is created and ready to manage the behavior of the new flow when you add the flow in the `_factories` array.

The controller connects View events with Model operations and updates the View with the results.

### 4. Application registration

The new MVC components are composed by `Application` in `src/core/application.py`.

The application is responsible for keeping the required component references alive.

### 5. Navigation

The feature is added to the application's navigation system inside `MainWindow` (`src/core/main_window.py`).

## External API integrations

External services are isolated inside the `providers` package.

The intended architecture is:

```text
Model
  │
  ▼
Provider (HttpClient)
  │
  ▼
QNetworkAccessManager
  │
  ▼
External REST API
```

`HttpClient` (`src/providers/http/http_client.py`) provides asynchronous HTTP requests using Qt's networking stack.

## Design principles

The project follows several principles:

* **KISS** — Prefer simple solutions when they are sufficient.
* **YAGNI** — Avoid implementing infrastructure before it is actually needed.
* **Separation of responsibilities** — Each component should have a clear responsibility.
* **High cohesion** — Related functionality should remain together.
* **Low coupling** — Components should depend on abstractions and stable interfaces where appropriate.
* **Incremental architecture** — The architecture should evolve with the real needs of the application.
* **Testability** — Business logic should remain testable independently from the graphical interface.

## Project status / roadmap

The project is currently in an active skeleton stage with key base features implemented.

### Completed

* [x] PySide6 application base.
* [x] Main application window with navigation container (`MainWindow`).
* [x] `QStackedWidget` navigation container.
* [x] MVC base classes (`Model`, `BaseView`, `Controller`).
* [x] Feature views implemented (`Home`, `Logs`, `Settings`, `Route Designer`, `Video Uploader`).
* [x] Custom widgets (`CheckableComboBox`, `SpeedometerProgress`).
* [x] Centralized application lifecycle through `Application`.
* [x] Logging infrastructure (`src/core/logging.py`).
* [x] Configuration management (`src/core/config.py`).
* [x] Generic HTTP client infrastructure (`src/providers/http/http_client.py`).
* [x] Text binding utilities (`src/core/text_binder.py`).
* [x] Localization structure (`skeleton_en_US`, `skeleton_es_ES`).
* [x] PyInstaller configuration & cross-platform build scripts (`build.sh`, `build.ps1`).
* [x] Automated tests (pytest + pytest-qt test suite in `tests/`).
* [x] CI pipeline configuration.

### Planned

* [ ] Concrete external API provider integrations (YouTube, Instagram, TikTok).
* [ ] Expanded settings persistence.
* [ ] Packaging and distribution installer improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file.
