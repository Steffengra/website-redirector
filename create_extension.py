import zipfile

def create_extension():
    files_to_zip = [
        'manifest.json',
        'background.js',
        "settings.html",
        "settings.js",
    ]

    with zipfile.ZipFile('website-redirector.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            zipf.write(file)


if __name__ == "__main__":
    create_extension()
