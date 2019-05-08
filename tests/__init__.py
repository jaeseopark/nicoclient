def get_file_content_as_string(filename):
    full_path = 'tests/resources/' + filename
    with open(full_path, 'r') as f:
        return f.read()
