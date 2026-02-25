"""
FileIQ - Document Intelligence Bot
Main application entry point with multi-page support
"""

import streamlit as st

# Import page render functions
from pages.home import render_home
from pages.upload import render_upload
from pages.about import render_about
from pages.settings import render_settings


def main():
    """Main application entry point"""
    # Streamlit's multi-page routing handles page switching automatically
    # The individual pages (home.py, upload.py, about.py, settings.py)
    # will be rendered based on navigation
    pass


if __name__ == "__main__":
    main()
