#navigation_manager.py

class NavigationManager:
    def __init__(self):
        self.stack = []

    def navigate_to(self, board):
        self.stack.append(board)

    def go_back(self):
        if len(self.stack) > 1:
            self.stack.pop()
            return self.stack[-1]
        return None

    def get_current_board(self):
        return self.stack[-1] if self.stack else None
    
    def get_navigation_stack(self):
        return self.stack
    
    def navigate_to_index(self, index):
        if 0 <= index < len(self.stack):
            self.stack = self.stack[:index + 1]
            return self.stack[-1]
        return None