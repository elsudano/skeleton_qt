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
* [Adding a new feature](#adding-a-new-feature)
* [External API integrations](#external-api-integrations)
* [Project status / roadmap](#project-status--roadmap)
* [License](#license)

## Project goal

The purpose of this project is to provide a reusable starting point for developing cross-platform applications with Python and Qt.

The skeleton provides:

* A structured **MVC architecture**.
* A permanent main application window.
* Internal navigation using `QStackedWidget`.
* Centralized application lifecycle management.
* Independent Models, Views and Controllers for each feature.
* A generic core layer for infrastructure shared by the application.
* A provider layer for external service integrations.
* Qt-based HTTP communication through `QNetworkAccessManager`.
* Localization support using Qt `.ts` and `.qm` translation files.
* PyInstaller support for creating distributable applications.
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
* Hosting the application's navigation container.

The main window remains alive while the user navigates between different features.

### View

Views contain the graphical user interface.

A View is responsible for:

* Creating Qt widgets.
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
* Data processing.
* Calculations.
* Validation.
* Communication with providers when appropriate.

Models must not manipulate Qt widgets directly.

### Provider

Providers isolate integrations with external services.

For example:

```text
providers/
├── youtube/
├── instagram/
└── tiktok/
```

Each provider contains the implementation required to communicate with its corresponding external service.

Provider-specific logic must not leak into the generic application infrastructure.

### Core

The `core` package contains infrastructure shared by the application.

Examples include:

* Application lifecycle.
* Configuration.
* HTTP infrastructure.
* Logging.
* Error handling.
* Shared application services.

The core layer must remain generic and must not contain provider-specific business logic.

## Repository structure

```text
.
├── main.py
├── requirements.txt
├── skeleton_qt.spec
│
├── resources/
│   └── translations/
│       ├── skeleton_es.ts
│       └── skeleton_en.ts
│
└── src/
    ├── __init__.py
    │
    ├── core/
    │   ├── application.py
    │   ├── config.py
    │   └── ...
    │
    ├── models/
    │   ├── model.py
    │   └── ...
    │
    ├── controllers/
    │   ├── controller.py
    │   └── ...
    │
    ├── views/
    │   ├── base_view.py
    │   ├── main_window.py
    │   └── ...
    │
    └── providers/
        ├── youtube/
        ├── instagram/
        └── tiktok/
```

## Technologies

### Python

The application is developed using Python.

### PySide6

PySide6 provides the Qt bindings used for:

* Graphical user interfaces.
* Signals and slots.
* Application lifecycle.
* Networking.
* Future platform-specific Qt functionality.

### Qt Networking

External REST APIs are intended to be accessed using Qt's networking infrastructure, primarily `QNetworkAccessManager`.

The project intentionally avoids coupling the application to provider-specific Python SDKs.

### PyInstaller

PyInstaller is used to package the application into distributable executables.

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

The project includes a PyInstaller specification file:

```text
skeleton_qt.spec
```

Build the application with:

```bash
pyinstaller --clean --noconfirm skeleton_qt.spec
```

The generated application will be placed in the `dist/` directory.

During development, the PyInstaller configuration keeps the console enabled to make debugging easier.

## Localization

The application is designed to use Qt's translation system.

Translation source files use the `.ts` format:

```text
resources/translations/
├── skeleton_es.ts
└── skeleton_en.ts
```

Compiled translation files use the `.qm` format.

User-visible strings should use Qt's translation mechanism:

```python
self.tr("Show welcome message")
```

The translation workflow is based on Qt tools such as:

```text
pyside6-lupdate
pyside6-lrelease
```

Runtime language switching may be added later.

## Adding a new feature

New application features should follow the MVC structure.

For example, a feature called `settings` would normally contain:

```text
src/
├── models/
│   └── settings_model.py
│
├── controllers/
│   └── settings_controller.py
│
└── views/
    └── settings_view.py
```

### 1. Model

Create a model derived from the base `Model` class.

The model contains the application's logic for the feature.

### 2. View

Create a view derived from `BaseView`.

The view contains the graphical interface and emits signals for user actions.

### 3. Controller

Create a controller derived from `Controller`.

The controller connects View events with Model operations and updates the View with the results.

### 4. Application registration

The new MVC components are composed by `Application`.

The application is responsible for keeping the required component references alive.

### 5. Navigation

The feature is added to the application's navigation system.

Views are not required to be created all at application startup. As the navigation system evolves, views can be created on demand when appropriate.

## External API integrations

External services are isolated inside the `providers` package.

The intended architecture is:

```text
Model
  │
  ▼
Provider
  │
  ▼
HTTP infrastructure
  │
  ▼
External REST API
```

For example:

```text
UploadModel
    │
    ▼
YouTubeProvider
    │
    ▼
QNetworkAccessManager
    │
    ▼
YouTube REST API
```

Provider implementations should contain the service-specific API knowledge.

The generic HTTP infrastructure must remain independent from YouTube, Instagram, TikTok or any other specific provider.

## Design principles

The project follows several principles:

* **KISS** — Prefer simple solutions when they are sufficient.
* **YAGNI** — Avoid implementing infrastructure before it is actually needed.
* **Separation of responsibilities** — Each component should have a clear responsibility.
* **High cohesion** — Related functionality should remain together.
* **Low coupling** — Components should depend on abstractions and stable interfaces where appropriate.
* **Incremental architecture** — The architecture should evolve with the real needs of the application.
* **Testability** — Business logic should remain testable independently from the graphical interface.

Patterns and abstractions should only be introduced when they provide a concrete benefit to the project.

## Project status / roadmap

The project is currently in its initial skeleton development stage.

### Completed

* [x] PySide6 application base.
* [x] Main application window.
* [x] `QStackedWidget` navigation container.
* [x] MVC base classes.
* [x] Initial Home MVC implementation.
* [x] Centralized application lifecycle through `Application`.
* [x] Initial localization structure.
* [x] PyInstaller configuration.

### Planned

* [ ] Improve the application navigation system.
* [ ] Lazy creation of application views.
* [ ] Generic HTTP infrastructure.
* [ ] Error handling infrastructure.
* [ ] Logging infrastructure.
* [ ] Configuration management.
* [ ] Automated tests.
* [ ] YouTube provider.
* [ ] Instagram provider.
* [ ] TikTok provider.
* [ ] Complete localization workflow.
* [ ] Packaging and distribution improvements.
* [ ] Evaluate Android support.

The roadmap is intentionally incremental. New infrastructure should be introduced when it is required by an actual application feature.

## License

This project is currently under development. check the [LICENSE](LICENSE) file
