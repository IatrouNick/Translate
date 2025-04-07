
import sys
import os

def read_params():
    try:
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
    return mapping.get(type_str.strip(), type_str.strip())

def resolve_path(filename):
    return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), filename)

def is_cp1253(input_file):
    try:
        with open(resolve_path(input_file), 'r', encoding='cp1253') as f:
            f.read()
        return True
    except UnicodeDecodeError:
        return False

def detect_encoding(input_file):
    import chardet
    with open(resolve_path(input_file), 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        print(f"📌 Detected encoding: {result['encoding']} (confidence {result['confidence']:.2f})")
        return result['encoding'] or 'utf-8'

def convert_file(input_file, output_file, input_encoding):
    try:
        input_path = resolve_path(input_file)
        output_path = resolve_path(output_file)

        with open(input_path, 'r', encoding=input_encoding, errors='replace') as f:
            content = f.read()
        content = content.lstrip('\ufeff')

        with open(output_path, 'w', encoding='cp1253', errors='replace') as f:
            f.write(content)

        print(f"✅ Conversion successful! Saved to:\n{output_path}")
    except Exception as e:
        print(f"❌ Conversion failed: {e}")

def main():
    args = sys.argv[1:]

    if len(args) >= 2:
        input_file = args[0]
        output_file = args[1]
        input_encoding = get_encoding_from_type(args[2]) if len(args) >= 3 else (
            'cp1253' if is_cp1253(input_file) else detect_encoding(input_file)
        )
        if input_encoding == 'cp1253':
            name, ext = os.path.splitext(output_file)
            output_file = f"{name}_ANSI{ext}"
            print(f"📁 Output file renamed to: {output_file}")
    else:
        params = read_params()
        if len(params) < 2:
            print("❗ param.txt is missing required parameters.")
            return
        input_file = params[0]
        output_file = params[1]
        if len(params) >= 3:
            input_encoding = get_encoding_from_type(params[2])
        else:
            if is_cp1253(input_file):
                input_encoding = 'cp1253'
                name, ext = os.path.splitext(output_file)
                output_file = f"{name}_ANSI{ext}"
                print(f"📁 Output file renamed to: {output_file}")
            else:
                input_encoding = detect_encoding(input_file)

    convert_file(input_file, output_file, input_encoding)

if __name__ == "__main__":
    main()
