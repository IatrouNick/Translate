import sys
import os

def read_params():
    try:
        with open("param.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            return lines
    except Exception as e:
        print(f"Error reading param.txt: {e}")
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
        with open(input_file, 'r', encoding=input_encoding) as f:
            content = f.read()
        with open(output_file, 'w', encoding='cp1252', errors='replace') as f:
            f.write(content)
        print(f"✅ Conversion successful! Saved to {output_file}")
    except Exception as e:
        print(f"❌ Conversion failed: {e}")

def detect_encoding(input_file):
    import chardet
    with open(input_file, 'rb') as f:
        raw_data = f.read()
        detected = chardet.detect(raw_data)
        print(f"📌 Detected encoding: {detected['encoding']}")
        return detected['encoding']

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
