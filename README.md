# KanBox - Nested KanBan Board Productivity App

KanBox is a unique productivity application centered around Nested KanBan Boards, offering a powerful and flexible way to organize tasks, projects, and workflows. Unlike traditional to-do lists, KanBox lets you create hierarchies of boards within boards, making it the ideal choice for managing complex, multi-level projects.

---

## Features
- **Nested KanBan Boards**: Create and navigate through hierarchical boards for comprehensive task management.
- **Project Management**: Add, remove, and manage projects with ease.
- **Customizable Boards**: Add columns, cards, and descriptions to tailor your workflow.
- **Breadcrumb Navigation**: Effortlessly track and navigate through your board hierarchy.
- **State Persistence**: Your projects, boards, and tasks are saved and restored automatically.

---

## Installation

### Prerequisites
- Python 3.8+ installed
- `PySide6` library for GUI components
- `pip` for installing dependencies

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/kanbox.git
   cd kanbox
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python main.py
   ```

---

## Usage

### Launching KanBox
Run the application using:
```bash
python main.py
```

### Creating a New Project
1. Click **Add** in the sidebar.
2. Enter the project name and click **OK**.

### Managing Boards
- **Add Columns**: Click **Add Column** in the board view.
- **Add Cards**: Use the **Add Card** button within a column.
- **Navigate**: Use breadcrumbs at the bottom of the board view to navigate between nested boards.
- **Edit Card or Column**: Right-click on a card or column for more options (e.g., rename, delete, reorder)

### Saving and Loading
KanBox automatically saves your work in `kanbox_data.json` and restores the last open project upon startup.

---

## Development

### Folder Structure
```
app/
│
├── core/             # Core logic (AppManager, StateManager, NavigationManager)
├── models/           # Data models (Board, Project, Card, ListColumn)
├── ui/               # UI components (Sidebar, BoardView, CardView, etc.)
├── assets/           # Styles and dialogues
│
main.py               # App entry point
requirements.txt      # Python dependencies
README.md             # Project README
```

### Key Components
1. **`AppManager`**: Manages the application state and navigation.
2. **`NavigationManager`**: Handles hierarchical board navigation.
3. **`StateManager`**: Saves and restores project state.
4. **UI Components**: Built with `PySide6` for an interactive experience.

---

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Submit a pull request.

---

## License
KanBox is licensed under the [MIT License](LICENSE).

---

## Contact
For support, feature requests, or contributions, reach out at:
- Email: [ffej1999@gmail.com](mailto:ffej1999@gmail.com)
- GitHub: [murples1999](https://github.com/murples1999)
