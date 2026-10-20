import json

def parse_antojitos_endpoints():
    with open("config/openapi_schema.json", "r", encoding="utf-8") as f:
        schema = json.load(f)
        
    paths = schema.get("paths", {})
    antojitos_paths = {path: methods for path, methods in paths.items() if "/antojitos" in path}
    
    print("--- antojitos express specific endpoints ---")
    for path, methods in antojitos_paths.items():
        for method, details in methods.items():
            summary = details.get("summary", "No summary")
            parameters = [p.get("name") for p in details.get("parameters", [])]
            print(f"[{method.upper()}] {path}")
            print(f"  Summary: {summary}")
            print(f"  Params:  {parameters}\n")

if __name__ == "__main__":
    parse_antojitos_endpoints()