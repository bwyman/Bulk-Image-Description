# main.py

import argparse
import os
from importlib import import_module
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process CSV file')
    parser.add_argument('-org', '--organization', type=str, required=True,
                        help='Organization name (e.g., CMA, GOK, LACMA, MET, NGA)')
    parser.add_argument('-ai', '--ai_name', type=str, required=True,
                        help='Name of the AI engine (e.g., openai, claude)')
    parser.add_argument('-images', '--download_images', action='store_true',
                        help='Download and resize images')
    parser.add_argument('input_csv_filename', type=str,
                        help='Filename of the input CSV file (assumed to be in the organization\'s "Source CSVs" directory)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    input_csv_filename = args.input_csv_filename
    organization = args.organization
    ai_name = args.ai_name
    
    if ai_name.lower() == 'claude':
        download_images = True
    else:
        download_images = args.download_images

    project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_csv_path = os.path.join(project_directory, organization, 'Source CSVs', input_csv_filename)

    try:
        csv_processor = import_module(f"{ai_name.lower()}_csv_processor")
        output_csv_path = csv_processor.process_csv(input_csv_path, organization, download_images)
    except FileNotFoundError:
        print(f"FileNotFoundError: No such file or directory: '{input_csv_path}'")
    except ModuleNotFoundError as e:
        print(f"ModuleNotFoundError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
