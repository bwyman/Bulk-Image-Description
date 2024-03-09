# Bulk Image Description

Bulk Image Description is a Python project that automates the process of generating alt text and descriptions for images in bulk using AI-powered image recognition and natural language processing.

## Features

- Extracts image URLs from CSV files containing artwork data
- Downloads and resizes images for processing
- Generates alt text and descriptions for images using OpenAI's GPT-4 Vision model
- Supports multiple AI engines (e.g., OpenAI, Claude) and prompt versions
- Modular and extensible design for easy integration with different organizations and AI engines

## Directory Structure

Bulk Image Description/
codebase/
- main.py
- claude_csv_processor.py
- openai_csv_processor.py
- orgs/
	- cma_image_utils.py
	- gok_image_utils.py
	- lacma_image_utils.py
	- met_image_utils.py
	- nga_image_utils.py
- openai_utils.py
- claude_utils.py
- image_processing.py
- config.py
- prompt_library.py

<org>/
- Source CSVs/
- Result CSVs/
- Source Images/
- Resized Images/

## Installation

1. Clone the repository:
	git clone https://github.com/your-username/bulk-image-description.git
2. Install the required dependencies:
	pip install -r requirements.txt
3. Set up the API keys and configurations:
	- Open `config.py` and update the `openai_config` dictionary with your OpenAI API key and other settings.
	- Add configurations for other AI engines (e.g., Claude) as needed.
4. Prepare the input CSV files:
	- Place the CSV files containing artwork data in the respective organization's "Source CSVs" directory (e.g., `CMA/Source CSVs/`).
	- Ensure that the CSV files have a column named "Obj URL" containing the URLs of the artwork pages.

## Usage and Execution
To generate alt text and descriptions for images, run the following command:
python codebase/main.py -org <organization> -ai <ai_name> [-images] <input_csv_filename>
	- `<organization>`: The name of the organization (e.g., nga).
	- `<ai_name>`: The name of the AI engine to use (e.g., openai, claude).
	- `-images` (optional): Flag to download and resize images. If not provided, only alt text and descriptions will be generated.
	- `<input_csv_filename>`: The filename of the input CSV file (assumed to be in the organization's "Source CSVs" directory).

Example:
python codebase/main.py -org nga -ai openai -images nga_example.csv

The generated alt text and descriptions will be saved in a new CSV file in the organization's "Result CSVs" directory, with the filename format: `<input_csv_filename>_<ai_name>_<prompt_version>_<timestamp>.csv`.## 

## Customization and Extension
- To add support for a new organization:
  1. Create a new `<organization>_image_utils.py` file in the `codebase/orgs/` directory.
  2. Implement the `extract_image_url` function in the new file to extract the image URL from the organization's artwork page.

- To add support for a new AI engine:
  1. Create a new `<ai_name>_utils.py` file in the `codebase/` directory.
  2. Implement the necessary functions (e.g., `call_ai_assistant`, `parse_response`) in the new file to interact with the AI engine's API.
  3. Create a new `<ai_name>_csv_processor.py` file in the `codebase/` directory, following the structure of existing CSV processor files.
  4. Update the `config.py` file to include the configuration for the new AI engine.

- To add or modify prompts:
  - Open the `prompt_library.py` file and add or modify prompts in the specified format.
  - Update the `openai_config['prompt_version']` or `claude_config['prompt_version']` value in the `config.py` file to use the desired prompt version.
  
## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).