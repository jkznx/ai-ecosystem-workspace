from pathlib import Path
import json
import sys

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
OPENAPI_FILE = ROOT_DIR / "docs" / "api" / "openapi.json"
OUTPUT_DIR = ROOT_DIR / "docs" / "api"

CSV_FILE = OUTPUT_DIR / "api-list.csv"
XLSX_FILE = OUTPUT_DIR / "api-list.xlsx"


HTTP_METHODS = {
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "head",
    "options",
    "trace",
}


def load_openapi() -> dict:
    if not OPENAPI_FILE.exists():
        print(f"OpenAPI file not found: {OPENAPI_FILE}")
        print("Run the FastAPI server and generate openapi.json first.")
        sys.exit(1)

    with OPENAPI_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def format_parameters(parameters: list | None) -> str:
    if not parameters:
        return ""

    result = []

    for parameter in parameters:
        name = parameter.get("name", "")
        location = parameter.get("in", "")
        required = parameter.get("required", False)

        result.append(
            f"{name} ({location}, "
            f"{'required' if required else 'optional'})"
        )

    return ", ".join(result)


def format_request_body(request_body: dict | None) -> str:
    if not request_body:
        return ""

    content = request_body.get("content", {})

    return ", ".join(content.keys())


def format_responses(responses: dict | None) -> str:
    if not responses:
        return ""

    result = []

    for status_code, response in responses.items():
        description = response.get("description", "")
        result.append(f"{status_code}: {description}")

    return " | ".join(result)


def extract_api_list(openapi: dict) -> list[dict]:
    rows = []

    for path, path_item in openapi.get("paths", {}).items():

        for method, operation in path_item.items():

            if method.lower() not in HTTP_METHODS:
                continue

            tags = operation.get("tags", [])

            rows.append(
                {
                    "Method": method.upper(),
                    "Path": path,
                    "Tags": ", ".join(tags),
                    "Operation ID": operation.get("operationId", ""),
                    "Summary": operation.get("summary", ""),
                    "Description": operation.get("description", ""),
                    "Parameters": format_parameters(
                        operation.get("parameters")
                    ),
                    "Request Body": format_request_body(
                        operation.get("requestBody")
                    ),
                    "Responses": format_responses(
                        operation.get("responses")
                    ),
                }
            )

    return rows


def export_files(rows: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dataframe = pd.DataFrame(rows)

    dataframe = dataframe.sort_values(
        by=["Path", "Method"],
        ignore_index=True,
    )

    dataframe.to_csv(
        CSV_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    dataframe.to_excel(
        XLSX_FILE,
        index=False,
        sheet_name="API List",
    )

    print(f"API count: {len(dataframe)}")
    print(f"CSV:   {CSV_FILE}")
    print(f"Excel: {XLSX_FILE}")


def main() -> None:
    openapi = load_openapi()
    rows = extract_api_list(openapi)
    export_files(rows)


if __name__ == "__main__":
    main()
