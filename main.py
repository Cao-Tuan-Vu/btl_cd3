

from pathlib import Path
import subprocess
import sys


def run_streamlit_app():
    project_root = Path(__file__).resolve().parent
    app_path = project_root / "src" / "app.py"

    if not app_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file ứng dụng: {app_path}")

    command = [sys.executable, "-m", "streamlit", "run", str(app_path)]
    subprocess.run(command, check=False)


if __name__ == '__main__':
    run_streamlit_app()
