import os
import yaml

def generate_api_suggestions(openapi_data, output_dir):
    paths = openapi_data.get("paths", {})
    for path, path_info in paths.items():
        sanitized_path = path.replace("/", "_").replace("{", "_").replace("}", "_")
        path_dir = os.path.join(output_dir, f"Path_{path}")
        os.makedirs(path_dir, exist_ok=True)
        for http_method, method_info in path_info.items():
            method_file_path = os.path.join(path_dir, f"HTTP_Method_{http_method}.txt")
            with open(method_file_path, 'w') as method_file:
                method_file.write(f"API Path: {path}\n")
                method_file.write(f"HTTP Method: {http_method}\n")
                tags = method_info.get("tags", [])
                method_file.writelines([f"Tag: {tag}\n" for tag in tags])
                summary = method_info.get("summary", "")
                method_file.write(f"Summary: {summary}\n")
                description = method_info.get("description", "")
                method_file.write(f"Description: {description}\n")
                parameters = method_info.get("parameters", [])
                for param in parameters:
                    ref = param.get("$ref", "")
                    if ref:
                        method_file.write(f"Parameter Reference: {ref}\n")
                responses = method_info.get("responses", {})
                for response_code, response_info in responses.items():
                    description = response_info.get("description", "")
                    method_file.write(f"Response {response_code}: {description}\n")

def create_entry_text_files(yaml_data, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)

        generate_api_suggestions(yaml_data, output_dir)

    except Exception as e:
        print(f"An error occurred: {e}")

def process_openapi_yaml(yaml_file, output_dir):
    try:
        with open(yaml_file, 'r') as file:
            yaml_data = yaml.safe_load(file)

        create_entry_text_files(yaml_data, output_dir)

        return "YAML data processed successfully."

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

input_yaml_file = '/api-docs-v1-external(1).yaml'
output_directory = '/x-tag_info'

result = process_openapi_yaml(input_yaml_file, output_directory)

if result:
    print(result)
else:
    print("Processing failed.")
