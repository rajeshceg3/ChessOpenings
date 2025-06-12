# Chess Openings Dashboard

This project is a Python Streamlit application designed to display information about various chess openings. It allows users to browse, filter, and search for openings, view their details (including move sequences and descriptions), and visualize the opening moves on a chessboard.

## Features

- Browse a curated list of chess openings.
- Filter openings by ECO code.
- Search for openings by name.
- View details for each opening: ECO code, name, move sequence, and a brief description.
- Interactive chessboard to visualize the selected opening's moves (step through with Previous/Next buttons).
- Summary statistics in the sidebar.

## Setup and Installation

1.  **Clone the repository (if applicable) or download the files.**

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    Make sure you have `chess_openings.csv`, `dashboard.py`, and `requirements.txt` in the same directory.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run dashboard.py
    ```
    This will typically open the dashboard in your web browser.

## Data Source

The chess opening data (`chess_openings.csv`) was curated based on information from various chess resources, including Wikipedia and PGN Mentor.
The PGN parsing and board logic uses the `python-chess` library.
The dashboard is built with `streamlit` and uses `pandas` for data manipulation.
