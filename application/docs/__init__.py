"""Markdown documentation blueprint."""
from __future__ import annotations

import os
import re

from flask import Blueprint, abort, current_app, jsonify

from application.utils.decorators import permission_required_api

docs = Blueprint("docs", __name__, url_prefix="/api/docs")

_DOC_SLUG_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def _docs_directory() -> str:
    base_dir = current_app.config.get("BASEDIR")
    return os.path.join(base_dir, "docs", "content")


def _slug_to_title(slug: str) -> str:
    words = re.split(r"[-_]+", slug)
    return " ".join(word.capitalize() for word in words if word)


def _list_markdown_files(directory: str) -> list[dict[str, str]]:
    if not os.path.isdir(directory):
        return []

    files = []
    for entry in sorted(os.listdir(directory)):
        if not entry.lower().endswith(".md"):
            continue
        slug = entry[:-3]
        files.append({"slug": slug, "title": _slug_to_title(slug)})
    return files


@docs.get("/")
@permission_required_api()
def list_docs():
    """Return a list of available markdown documents."""
    directory = _docs_directory()
    documents = _list_markdown_files(directory)
    return jsonify(documents)


@docs.get("/<string:slug>")
@permission_required_api()
def get_doc(slug: str):
    """Return the markdown content of a specific document."""
    if not _DOC_SLUG_PATTERN.match(slug):
        abort(404)

    directory = _docs_directory()
    file_path = os.path.join(directory, f"{slug}.md")

    if not os.path.isfile(file_path):
        abort(404)

    with open(file_path, "r", encoding="utf-8") as markdown_file:
        content = markdown_file.read()

    return jsonify({
        "slug": slug,
        "title": _slug_to_title(slug),
        "content": content,
    })
