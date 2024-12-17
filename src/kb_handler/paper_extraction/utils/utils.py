import io
import os
import regex
import requests
import tarfile
import warnings


INVALID_FILE_CHARS_PATTERN = regex.compile(r'[<>:"/\\|?*\x00-\x1F]')


def extract_online_zip(url, extraction_dir):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_bytes = io.BytesIO()
        for chunk in response.iter_content(chunk_size=8192):
            file_bytes.write(chunk)
        file_bytes.seek(0)
        with tarfile.open(fileobj=file_bytes, mode='r:gz') as tar_ref:
            tar_ref.extractall(extraction_dir)
        return extraction_dir
    warnings.warn(f'Failed to download zip from {url}')
    return None


def dir_files(dir_path):
    file_list = []
    for root, directories, files in os.walk(dir_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_list.append(filepath)
    return file_list


def dir_extension_files(dir_path, extension='.tex'):
    all_files = dir_files(dir_path)
    extension_files = [path for path in all_files if path.endswith(extension)]
    return extension_files


def sanitize_filename(filename: str, replace_with: str = '') -> str:
    filename = INVALID_FILE_CHARS_PATTERN.sub(replace_with, filename)
    filename = filename.replace(' ', '_')
    filename = filename.lower()
    return filename[:255]