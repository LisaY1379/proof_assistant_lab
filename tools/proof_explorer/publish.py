"""Build the static GitHub Pages homepage from the proof explorer sources."""

from pathlib import Path
import shutil


def main():
    source = Path(__file__).resolve().parent
    docs = source.parents[1] / "docs"
    assets = docs / "proof-explorer"
    assets.mkdir(parents=True, exist_ok=True)

    homepage = docs / "index.html"
    library = docs / "proof-strategy-viewer.html"
    # Preserve the original public library once, before replacing its homepage.
    if homepage.exists() and not library.exists():
        if "Proof Strategy Public Viewer" not in homepage.read_text():
            raise RuntimeError("Unexpected existing homepage; inspect it before publishing.")
        shutil.copyfile(homepage, library)

    filenames = ("styles.css", "protocol.css", "protocol.js", "protocol-reference.css", "proof.js", "written-proof.js", "app.js")
    for filename in filenames:
        shutil.copyfile(source / filename, assets / filename)
    for page in ("index.html", "protocol.html", "protocol-reference.html"):
        html = (source / page).read_text()
        for filename in filenames:
            html = html.replace(f'"{filename}"', f'"proof-explorer/{filename}"')
        if page == "index.html" and library.exists():
            html = html.replace(
                '<a href="protocol.html">Our protocol</a>',
                '<a href="proof-strategy-viewer.html">Proof library</a> &nbsp; · &nbsp; '
                '<a href="protocol.html">Our protocol</a>',
            )
        (docs / page).write_text(html)
    print(f"Built GitHub Pages homepage: {homepage}")


if __name__ == "__main__":
    main()
