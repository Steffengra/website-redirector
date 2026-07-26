import zipfile
import json
from hashlib import sha256
from pathlib import Path


def create_extension():

    def _get_current_version():
        with open(extension_manifest_file_name, "r", encoding="utf-8") as _file:
            _manifest = json.load(fp=_file)
        return _manifest["version"]

    def _get_updates_manifest():
        with open(updates_manifest_file_name, "r", encoding="utf-8") as _file:
            return json.load(fp=_file)

    def _check_version_already_exists():
        if extension_file_path.exists():
            raise PermissionError("Extension with this version number already exists. Update version number in manifest.json.")

        if current_version in [
            update["version"]
            for update in updates_manifest["addons"]["{ec00d5a7-84dc-4539-80c0-7fb4cf9d37c4}"]["updates"]
        ]:
            raise PermissionError("Extension with this version number already exists. Update version number in manifest.json.")

    def _create_extension_file():
        with zipfile.ZipFile(extension_file_name, 'w', zipfile.ZIP_DEFLATED) as _zipf:
            for _file in files_to_zip:
                _zipf.write(_file)

    def _update_updates_manifest():
        _past_updates = updates_manifest["addons"]["{ec00d5a7-84dc-4539-80c0-7fb4cf9d37c4}"]["updates"]
        _extension_file_hash = sha256(extension_file_path.read_bytes())
        current_update = {
            "version": current_version,
            "update_link": f"https://github.com/Steffengra/website-redirector/releases/download/{current_version}/{extension_file_name}",
            "update_hash": f"sha256:{_extension_file_hash.hexdigest()}",
        }
        updates_manifest["addons"]["{ec00d5a7-84dc-4539-80c0-7fb4cf9d37c4}"]["updates"] = _past_updates + [current_update]
        with open(updates_manifest_file_name, "w", encoding="utf-8") as _file:
            json.dump(obj=updates_manifest, fp=_file, indent=5)


    extension_manifest_file_name = "manifest.json"
    updates_manifest_file_name = "updates.json"

    current_version = _get_current_version()

    extension_file_name = f'website-redirector-{current_version}.xpi'
    extension_file_path = Path(extension_file_name)

    updates_manifest = _get_updates_manifest()
    _check_version_already_exists()

    files_to_zip = [
        'manifest.json',
        'background.js',
        "settings.html",
        "settings.js",
    ]
    _create_extension_file()
    _update_updates_manifest()

    print(f"--------------REMINDER--------------\nUpdate the new .xpi file to github as a release with the correct tag: {current_version}")


if __name__ == "__main__":
    create_extension()
