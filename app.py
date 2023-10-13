import os
import yaml

def generate_api_suggestions(openapi_data, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)

        paths = openapi_data.get("paths", {})
        for path, path_info in paths.items():
            summary = path_info.get("summary", "NoSummary")
            path_file_name = f"{summary.strip().replace(' ', '_')}_api_suggestions.txt"
            path_file_path = os.path.join(output_dir, path_file_name)

            with open(path_file_path, 'w') as path_file:
                path_file.write(f"Path: {path}\n")
                for http_method, method_info in path_info.items():
                    path_file.write(f"  - HTTP Method: {http_method}\n")
                    tags = method_info.get("tags", [])
                    path_file.write(f"    - Tags: {', '.join(tags)}\n")
                    path_file.write(f"    - Summary: {summary}\n")
                    description = method_info.get("description", "")
                    path_file.write(f"    - Description: {description}\n")
                    parameters = method_info.get("parameters", [])
                    for param in parameters:
                        ref = param.get("$ref", "")
                        if ref:
                            path_file.write(f"    - Parameter Reference: {ref}\n")
                    responses = method_info.get("responses", {})
                    for response_code, response_info in responses.items():
                        description = response_info.get("description", "")
                        path_file.write(f"    - Response {response_code}: {description}\n")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_entry_text_files(yaml_data, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)

        info = yaml_data.get("info", {})
        with open(os.path.join(output_dir, 'info.txt'), 'w') as info_file:
            info_file.write(f"API Title: {info.get('title', '')}\n")
            info_file.write(f"API Version: {info.get('version', '')}\n")
            info_file.write(f"API Description:\n{info.get('description', '')}\n")

        tag_groups = yaml_data.get("x-tagGroups", [])
        for tag_group in tag_groups:
            name = tag_group.get("name", "").strip()
            if name:
                tag_dir = os.path.join(output_dir, name)
                os.makedirs(tag_dir, exist_ok=True)
                with open(os.path.join(tag_dir, 'tags.txt'), 'w') as tags_file:
                    tags = tag_group.get("tags", [])
                    for tag in tags:
                        tags_file.write(f"{tag}\n")

        servers = yaml_data.get("servers", [])
        with open(os.path.join(output_dir, 'servers.txt'), 'w') as servers_file:
            for server in servers:
                url = server.get("url", "")
                description = server.get("description", "")
                servers_file.write(f"URL: {url}\n")
                servers_file.write(f"Description: {description}\n")

        components = yaml_data.get("components", {})
        with open(os.path.join(output_dir, 'components.txt'), 'w') as components_file:
            security_schemes = components.get("securitySchemes", {})
            for scheme_name, scheme_info in security_schemes.items():
                scheme_type = scheme_info.get("type", "")
                scheme_scheme = scheme_info.get("scheme", "")
                components_file.write(f"- Security Scheme: {scheme_name}\n")
                components_file.write(f"  - Type: {scheme_type}\n")
                components_file.write(f"  - Scheme: {scheme_scheme}\n")
            components_file.write("\n")

        parameters = yaml_data.get("components", {}).get("parameters", {})
        with open(os.path.join(output_dir, 'parameters.txt'), 'w') as parameters_file:
            for param_name, param_info in parameters.items():
                param_description = param_info.get("description", "")
                param_required = param_info.get("required", False)
                param_name_in = param_info.get("in", "")
                schema_ref = param_info.get("schema", {}).get("$ref", "")
                parameters_file.write(f"- Parameter Name: {param_name}\n")
                parameters_file.write(f"  - Description:\n{param_description}\n")
                parameters_file.write(f"  - Required: {param_required}\n")
                parameters_file.write(f"  - Location (in): {param_name_in}\n")
                parameters_file.write(f"  - Schema Reference: {schema_ref}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

def process_openapi_yaml(yaml_file, output_dir):
    try:
        with open(yaml_file, 'r') as file:
            yaml_data = yaml.safe_load(file)

        create_entry_text_files(yaml_data, output_dir)
        generate_api_suggestions(yaml_data, output_dir)

        return "YAML data processed successfully."

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

input_yaml_file = '/home/hemanth/Desktop/YAMLconversion/api-docs-v1-external(1).yaml'  
output_directory = '/home/hemanth/Desktop/YAMLconversion/x-tag_info' 

result = process_openapi_yaml(input_yaml_file, output_directory)

if result:
    print(result)
else:
    print("Processing failed.")
