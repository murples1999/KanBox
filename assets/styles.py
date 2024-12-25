#styles.py

class Styles:
    # Card styles
    card_style = """
    QFrame {
        background-color: #7d7f7c;
        border: 1px solid #000000;
        border-radius: 8px;
        padding: 8px;
        margin: 2px;
    }
    QLabel {
        font-size: 14px;
        color: #333;
        padding: 4px;
        text-align: left;
    }
    """

    # Column styles
    column_style = """
    QWidget {
        background-color: transparent;
        margin: 0px;  
    }
    """

    column_title_style = """
    QLabel {
        font-size: 16px;
        font-weight: bold;
        color: #ffffff;
        margin: 16px;
    }
    """

    # Add Card Button styles
    add_card_button_style = """
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px;
        margin-top: 4px;  /* Slight margin to separate from cards */
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    """

    # Add Column Button styles
    add_column_button_style = """
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 20px; /* More space inside the button */
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    """

    #Project Button styles
    project_button_style = """
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px;
        margin: 8px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    """

    # Board styles
    board_style = """
    QWidget {
        background-color: transparent;
        
    }
    """
    #border: 1px solid #000000;

    #Context Menu Styles
    context_menu_style = """
    QMenu {
        background-color: #2c2c2c;
        color: white;
        border: 1px solid #555;
        padding: 6px;
        border-radius: 5px;
    }
    QMenu::item {
        padding: 8px 20px;
        margin: 0px;
        background-color: transparent;
    }
    QMenu::item:selected {
        background-color: #4CAF50;
        color: white;
    }
    """

    #Dialog Styles
    dialog_style = """
    QDialog {
        background-color: #2c2c2c;
        border: 1px solid #555;
        border-radius: 5px;
        padding: 10px;
    }
    QLabel {
        color: white;
        font-size: 14px;
    }
    QPlainTextEdit {
        background-color: #3c3c3c;
        border: 1px solid #555;
        border-radius: 4px;
        color: white;
        font-size: 14px;
        padding: 4px;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    """

    #breadcrumb_styles
    breadcrumb_button_style = """
    QPushButton {
        border: none;
        color: white;
        text-decoration: underline;
    }
    QPushButton:hover {
        color: red;
    }
    """