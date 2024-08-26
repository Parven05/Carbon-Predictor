def load_text(file_path):
    """Load the welcome text from the specified file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading text from {file_path}: {e}")
        return ""
