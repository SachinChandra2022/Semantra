import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import backend.preprocess_utils  # Change this based on your actual file/module structure

RAW_DATA_DIR = 'data/raw'
PROCESSED_DATA_DIR = 'data/processed'
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def preprocess_all_files():
    print(f"Checking for files in: {os.path.abspath(RAW_DATA_DIR)}")

    try:
        raw_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.html') or f.endswith('.txt')]
        print("Files found:", raw_files)
    except Exception as e:
        print("Error reading raw files:", e)
        return

    if not raw_files:
        print("No .html or .txt files found in raw data directory.")
        return

    for filename in raw_files:
        input_path = os.path.join(RAW_DATA_DIR, filename)
        output_path = os.path.join(PROCESSED_DATA_DIR, filename.replace('.html', '.txt'))

        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            clean_text = preprocess_utils.preprocess_html(html_content)
            print(f"Cleaned text preview (first 200 chars):\n{clean_text[:200]}")  # Preview output

            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(clean_text)

            print(f"✅ Processed: {filename} → {output_path}")

        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")

if __name__ == "__main__":
    preprocess_all_files()