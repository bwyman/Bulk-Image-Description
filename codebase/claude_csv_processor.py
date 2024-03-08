# claude_csv_processor.py
import csv
import os
from datetime import datetime, timedelta
import time
from tqdm import tqdm
from importlib import import_module
from image_processing import download_and_resize_image
from config import claude_config

def process_csv(input_csv_path, organization, download_images=False):
    start_time = time.time()
    
    base_name = os.path.splitext(os.path.basename(input_csv_path))[0]
    prompt_version = claude_config['prompt_version']
    output_csv_name = f"{base_name}_claude_{prompt_version}_{datetime.now().strftime('%Y%m%d%H%M')}.csv"

    project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create the 'Result CSVs' directory if it doesn't exist
    result_csvs_directory = os.path.join(project_directory, organization, 'Result CSVs')
    os.makedirs(result_csvs_directory, exist_ok=True)
    
    output_csv_path = os.path.join(result_csvs_directory, output_csv_name)

    try:
        image_utils = import_module(f"orgs.{organization.lower()}_image_utils")
        claude_utils = import_module("claude_utils")
    except ImportError as e:
        print(f"Error importing module: {e}")
        return None

    if download_images:
        source_images_directory = os.path.join(project_directory, organization, 'Source Images')
        resized_images_directory = os.path.join(project_directory, organization, 'Resized Images')
        os.makedirs(source_images_directory, exist_ok=True)
        os.makedirs(resized_images_directory, exist_ok=True)

    try:
        with open(input_csv_path, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames + ['Image URL', 'Alt Text (Short)', 'Alt Text (Long)', 'Image Description']

            with open(output_csv_path, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()

                total_objects = sum(1 for row in reader)
                infile.seek(0)
                next(reader)

                progress_bar = tqdm(total=total_objects, unit='obj', desc='Processing')

                for row in reader:
                    image_url = image_utils.extract_image_url(row['Obj URL'])
                    row['Image URL'] = image_url if image_url else 'Not Found'

                    if image_url:
                        if download_images:
                            image_filename = os.path.basename(image_url)
                            source_image_path = os.path.join(source_images_directory, image_filename)
                            resized_image_path = os.path.join(resized_images_directory, image_filename)
                            download_and_resize_image(image_url, source_image_path, resized_image_path)

                        response = claude_utils.call_claude_assistant(image_url)
                        if response:
                            parsed_responses = claude_utils.parse_response(response)
                            row['Alt Text (Short)'] = parsed_responses.get('alt_text_short', 'Error')
                            row['Alt Text (Long)'] = parsed_responses.get('alt_text_long', 'Error')
                            row['Image Description'] = parsed_responses.get('image_description', 'Error')
                        else:
                            row['Alt Text (Short)'] = row['Alt Text (Long)'] = row['Image Description'] = 'Error'

                    writer.writerow(row)
                    progress_bar.update(1)

                progress_bar.close()

    except FileNotFoundError:
        print(f"Error: Input CSV file '{input_csv_path}' not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied when accessing the input CSV file '{input_csv_path}'.")
        return None
    except Exception as e:
        print(f"Error processing CSV: {e}")
        return None

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_delta = timedelta(seconds=elapsed_time)
    time_str = str(elapsed_time_delta) if elapsed_time_delta.total_seconds() >= 3600 else time.strftime("%M:%S", time.gmtime(elapsed_time))
    print(f"Processing of {total_objects} objects done. Time to complete: {time_str}")
    
    return output_csv_path