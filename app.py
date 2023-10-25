import os
import yaml

def generate_api_suggestions(openapi_data, output_dir):
    paths = openapi_data.get("paths", {})
    for path, path_info in paths.items():
        sanitized_path = path.replace("/", "_").replace("{", "_").replace("}", "_")
        path_dir = os.path.join(output_dir, f"Path_{sanitized_path}")
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
                if http_method == "post":
                    request_body = method_info.get("requestBody", {})
                    if request_body:
                        content = request_body.get("content", {})
                        for content_type, content_info in content.items():
                            schema = content_info.get("schema", {})
                            if schema:
                                method_file.write("Request Body Schema:\n")
                                method_file.write(f"  Type: {schema.get('type', '')}\n")
                                required = schema.get('required', [])
                                if required:
                                    method_file.write("  Required:\n")
                                    method_file.writelines([f"    - {req}\n" for req in required])
                                properties = schema.get('properties', {})
                                if properties:
                                    method_file.write("  Properties:\n")
                                    for prop, prop_info in properties.items():
                                        prop_type = prop_info.get('type', '')
                                        prop_description = prop_info.get('description', '')
                                        method_file.write(f"    {prop}:\n")
                                        method_file.write(f"      Type: {prop_type}\n")
                                        method_file.write(f"      Description: {prop_description}\n")
                
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
