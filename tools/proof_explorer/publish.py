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

    html = (source / "index.html").read_text()
    for filename in ("styles.css", "proof.js", "written-proof.js", "app.js"):
        shutil.copyfile(source / filename, assets / filename)
        html = html.replace(f'"{filename}"', f'"proof-explorer/{filename}"')
    if library.exists():
        html = html.replace(
            '<a href="#about">About this proof</a>',
            '<nav aria-label="Site navigation"><a href="proof-strategy-viewer.html">Proof library</a>'
            ' &nbsp; · &nbsp; <a href="#about">About this proof</a></nav>',
        )
    homepage.write_text(html)
    print(f"Built GitHub Pages homepage: {homepage}")


if __name__ == "__main__":
    main()
