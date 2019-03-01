def get_file_content_as_string(filename):
    with open('tests/resources/' + filename, 'r') as f:
        return f.read()
