"""Script to pack the uniVRc extension into a standard .vsix archive without requiring Node.js or vsce."""
import os
import zipfile
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_JSON_FILE = os.path.join(BASE_DIR, "package.json")

def get_package_info():
    with open(PACKAGE_JSON_FILE, "r", encoding="utf-8") as f:
        pkg = json.load(f)
    version = pkg.get("version", "0.4.0")
    publisher = pkg.get("publisher", "univrc")
    name = pkg.get("name", "univrc")
    description = pkg.get("description", "Official uniVRc IntelliSense extension.")
    return name, version, publisher, description

CONTENT_TYPES_XML = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="png" ContentType="image/png" />
  <Default Extension="md" ContentType="text/markdown" />
  <Default Extension="js" ContentType="application/javascript" />
  <Default Extension="py" ContentType="text/x-python" />
  <Default Extension="g4" ContentType="text/plain" />
  <Default Extension="interp" ContentType="text/plain" />
  <Default Extension="tokens" ContentType="text/plain" />
  <Default Extension="vsixmanifest" ContentType="text/xml" />
</Types>
"""

def generate_vsix_manifest(name, version, publisher, description):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">
  <Metadata>
    <Identity Id="{name}" Version="{version}" Language="en-US" Publisher="{publisher}" />
    <DisplayName>uniVRc IntelliSense</DisplayName>
    <Description>{description}</Description>
    <Categories>Programming Languages,Linters,Snippets</Categories>
    <Icon>extension/icon.png</Icon>
  </Metadata>
  <Installation>
    <InstallationTarget Id="Microsoft.VisualStudio.Code" />
  </Installation>
  <Dependencies />
  <Assets>
    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true" />
    <Asset Type="Microsoft.VisualStudio.Services.Icons.Default" Path="extension/icon.png" Addressable="true" />
    <Asset Type="Microsoft.VisualStudio.Services.Content.Details" Path="extension/README.md" Addressable="true" />
  </Assets>
</PackageManifest>
""".strip()

def collect_files():
    files = [
        "package.json",
        "extension.js",
        "language-configuration.json",
        "README.md",
        "README-fa.md",
        "icon.png",
        os.path.join("syntaxes", "univrc.tmLanguage.json"),
        os.path.join("snippets", "univrc.json"),
    ]

    # Collect icons
    icons_dir = os.path.join(BASE_DIR, "icons")
    if os.path.isdir(icons_dir):
        for f in os.listdir(icons_dir):
            files.append(os.path.join("icons", f))

    # Collect server files (including antlr_gen)
    server_dir = os.path.join(BASE_DIR, "server")
    if os.path.isdir(server_dir):
        for root, dirs, filenames in os.walk(server_dir):
            # skip __pycache__
            if "__pycache__" in root:
                continue
            for fn in filenames:
                if fn.endswith(".pyc"):
                    continue
                rel_path = os.path.relpath(os.path.join(root, fn), BASE_DIR)
                files.append(rel_path)

    return sorted(list(set(files)))

def build():
    name, version, publisher, description = get_package_info()
    output_vsix = os.path.join(BASE_DIR, f"{name}-{version}.vsix")
    manifest_xml = generate_vsix_manifest(name, version, publisher, description)

    print(f"Building {output_vsix} (v{version}) ...")
    with zipfile.ZipFile(output_vsix, "w", zipfile.ZIP_DEFLATED) as zf:
        # Write root metadata
        zf.writestr("[Content_Types].xml", CONTENT_TYPES_XML.strip())
        zf.writestr("extension.vsixmanifest", manifest_xml)
        
        # Write extension payload
        for rel_path in collect_files():
            full_path = os.path.join(BASE_DIR, rel_path)
            if os.path.exists(full_path):
                arcname = "extension/" + rel_path.replace("\\", "/")
                zf.write(full_path, arcname)
                print(f"  Added {arcname}")
            else:
                print(f"  WARNING: File missing {full_path}")

    print(f"Successfully generated {output_vsix} ({os.path.getsize(output_vsix)} bytes).")
    return output_vsix

if __name__ == "__main__":
    build()
