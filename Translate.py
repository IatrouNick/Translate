import sys
import os

def read_params():
    try:
        # Use the script or .exe directory, not the current working directory
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        param_file_path = os.path.join(base_path, "param.txt")

        print(f"📂 Reading param.txt from: {param_file_path}")

        with open(param_file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            return lines
    except Exception as e:
        print(f"❌ Error reading param.txt: {e}")
        sys.exit(1)


def get_encoding_from_type(type_str):
    mapping = {
        "1": "utf-8",
        "2": "utf-16-le",
        "3": "utf-16-be"
    }
    return mapping.get(type_str.strip())

def convert_file(input_file, output_file, input_encoding):
    try:
        with open(resolve_path(input_file), 'r', encoding=input_encoding, errors='replace') as f:
            content = f.read()
        content = content.lstrip('\ufeff')  # Remove BOM if present

        # ✅ Save as UTF-8 with BOM (Excel friendly, Greek-safe)
        with open(resolve_path(output_file), 'w', encoding='utf-8-sig', errors='replace') as f:
            f.write(content)

        print(f"✅ Conversion successful! Saved to {output_file}")
    except Exception as e:
        print(f"❌ Conversion failed: {e}")


def detect_encoding(input_file):
    import chardet
    with open(resolve_path(input_file), 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        print(f"📌 Detected encoding: {result['encoding']} (confidence {result['confidence']:.2f})")
        return result['encoding'] or 'utf-8'  # fallback

def resolve_path(filename):
    return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), filename)

def main():
    args = sys.argv[1:]

    if len(args) >= 2:
        input_file = args[0]
        output_file = args[1]
        input_encoding = get_encoding_from_type(args[2]) if len(args) >= 3 else detect_encoding(input_file)
    else:
        params = read_params()
        if len(params) < 2:
            print("❗ param.txt is missing required parameters.")
            return
        input_file = params[0]
        output_file = params[1]
        input_encoding = get_encoding_from_type(params[2]) if len(params) >= 3 else detect_encoding(input_file)

    convert_file(input_file, output_file, input_encoding)

if __name__ == "__main__":
    main()
