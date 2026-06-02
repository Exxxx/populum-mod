"""Shared ComfyUI API helpers for COE5 sprite art tools."""
from __future__ import annotations

import copy
import json
import mimetypes
import random
import time
import uuid
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from coe5_sprite_prompts import SPRITE_NEGATIVE_PROMPT

TOOLS_DIR = Path(__file__).resolve().parent
DEFAULT_COMFYUI_URL = "http://127.0.0.1:8000"
WORKFLOW_TXT2IMG = TOOLS_DIR / "workflows" / "image_qwen_Image_2512_pop_tile_api.json"
WORKFLOW_EDIT = TOOLS_DIR / "workflows" / "image_qwen_image_edit_2509_icon_api.json"

# Qwen Image 2512 pop_tile workflow inject nodes
TXT2IMG_NODE_PROMPT = "197:180"
TXT2IMG_NODE_NEGATIVE = "197:195"
TXT2IMG_NODE_LATENT = "197:179"
TXT2IMG_NODE_SAMPLER = "197:194"
TXT2IMG_NODE_SAVE = "199"
TXT2IMG_NODE_PREFIX = "200"
TXT2IMG_NODE_LIGHTNING = "197:196"

# Qwen Image Edit 2509 icon workflow inject nodes
EDIT_NODE_PROMPT = "435"
EDIT_NODE_LOAD_IMAGE = "78"
EDIT_NODE_SAMPLER = "433:3"
EDIT_NODE_SAVE = "60"


def http_json(method: str, url: str, payload: dict | None = None, timeout: float = 120.0) -> Any:
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else None
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(detail)
            message = parsed.get("error", {}).get("message") or parsed.get("message") or detail
            node_errors = parsed.get("node_errors")
            if node_errors:
                message = f"{message}\n{json.dumps(node_errors, indent=2)}"
        except json.JSONDecodeError:
            message = detail or str(exc)
        raise RuntimeError(f"ComfyUI HTTP {exc.code}: {message}") from exc


def load_workflow(path: Path) -> dict[str, Any]:
    workflow = json.loads(path.read_text(encoding="utf-8"))
    return {k: v for k, v in workflow.items() if not k.startswith("_")}


def patch_txt2img_workflow(
    workflow: dict[str, Any],
    *,
    prompt: str,
    filename_prefix: str,
    output_dir: Path,
    width: int,
    height: int,
    seed: int | None = None,
    negative: str | None = None,
) -> dict[str, Any]:
    patched = copy.deepcopy(workflow)
    patched[TXT2IMG_NODE_PROMPT]["inputs"]["text"] = prompt
    if TXT2IMG_NODE_NEGATIVE in patched:
        patched[TXT2IMG_NODE_NEGATIVE]["inputs"]["text"] = negative or SPRITE_NEGATIVE_PROMPT
    patched[TXT2IMG_NODE_LATENT]["inputs"]["width"] = width
    patched[TXT2IMG_NODE_LATENT]["inputs"]["height"] = height
    patched[TXT2IMG_NODE_SAMPLER]["inputs"]["seed"] = (
        seed if seed is not None else random.randint(0, 2**63 - 1)
    )
    patched[TXT2IMG_NODE_SAVE]["inputs"]["output_path"] = output_dir.as_posix()
    patched[TXT2IMG_NODE_SAVE]["inputs"]["overwrite_mode"] = "prefix_as_filename"
    patched[TXT2IMG_NODE_PREFIX]["inputs"]["text"] = filename_prefix
    if TXT2IMG_NODE_LIGHTNING in patched:
        patched[TXT2IMG_NODE_LIGHTNING]["inputs"]["value"] = True
    return patched


def patch_edit_workflow(
    workflow: dict[str, Any],
    *,
    prompt: str,
    reference_image: str,
    seed: int | None = None,
) -> dict[str, Any]:
    patched = copy.deepcopy(workflow)
    patched[EDIT_NODE_PROMPT]["inputs"]["value"] = prompt
    patched[EDIT_NODE_LOAD_IMAGE]["inputs"]["image"] = reference_image
    patched[EDIT_NODE_SAMPLER]["inputs"]["seed"] = (
        seed if seed is not None else random.randint(0, 2**63 - 1)
    )
    patched[EDIT_NODE_SAVE]["inputs"]["filename_prefix"] = "coe5_edit"
    return patched


def queue_prompt(base_url: str, workflow: dict[str, Any], client_id: str) -> str:
    payload = {"prompt": workflow, "client_id": client_id}
    result = http_json("POST", f"{base_url.rstrip('/')}/prompt", payload)
    prompt_id = result.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"ComfyUI did not return prompt_id: {result}")
    node_errors = result.get("node_errors") or {}
    if node_errors:
        raise RuntimeError(f"ComfyUI node errors: {json.dumps(node_errors, indent=2)}")
    return prompt_id


def format_execution_error(status: dict[str, Any]) -> str:
    for event, payload in status.get("messages") or []:
        if event != "execution_error":
            continue
        node_id = payload.get("node_id", "?")
        node_type = payload.get("node_type", "?")
        message = (payload.get("exception_message") or "").strip()
        return f"{node_type} (node {node_id}): {message or payload}"
    return json.dumps(status.get("messages") or status, indent=2)


def wait_for_prompt(
    base_url: str,
    prompt_id: str,
    poll_seconds: float,
    timeout_seconds: float,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        history = http_json("GET", f"{base_url.rstrip('/')}/history/{prompt_id}", timeout=30.0)
        if prompt_id in history:
            entry = history[prompt_id]
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                raise RuntimeError(f"ComfyUI prompt failed: {format_execution_error(status)}")
            return entry
        time.sleep(poll_seconds)
    raise TimeoutError(f"Timed out waiting for prompt {prompt_id}")


def upload_image(base_url: str, path: Path, *, subfolder: str = "", image_type: str = "input") -> str:
    """Upload image to ComfyUI input folder; returns filename for LoadImage node."""
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    body_parts = [
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="image"; filename="{path.name}"\r\n'.encode(),
        f"Content-Type: {mime}\r\n\r\n".encode(),
        path.read_bytes(),
        f"\r\n--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="type"\r\n\r\n',
        f"{image_type}\r\n".encode(),
        f"--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="subfolder"\r\n\r\n',
        f"{subfolder}\r\n".encode(),
        f"--{boundary}--\r\n".encode(),
    ]
    body = b"".join(body_parts)
    req = Request(
        f"{base_url.rstrip('/')}/upload/image",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=120.0) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ComfyUI upload failed HTTP {exc.code}: {detail}") from exc
    name = result.get("name")
    if not name:
        raise RuntimeError(f"ComfyUI upload did not return name: {result}")
    return name


def find_saved_image(output_dir: Path, filename_prefix: str) -> Path | None:
    for ext in (".webp", ".png", ".jpg", ".jpeg"):
        exact = output_dir / f"{filename_prefix}{ext}"
        if exact.exists():
            return exact
        matches = sorted(output_dir.glob(f"{filename_prefix}*{ext}"))
        if matches:
            return matches[-1]
    return None


def extract_output_images(history_entry: dict[str, Any]) -> list[dict[str, Any]]:
    outputs = history_entry.get("outputs") or {}
    images: list[dict[str, Any]] = []
    for node_output in outputs.values():
        for img in node_output.get("images") or []:
            images.append(img)
    return images


def download_history_image(
    base_url: str,
    image_info: dict[str, Any],
    dest: Path,
) -> Path:
    params = urlencode(
        {
            "filename": image_info["filename"],
            "subfolder": image_info.get("subfolder", ""),
            "type": image_info.get("type", "output"),
        }
    )
    url = f"{base_url.rstrip('/')}/view?{params}"
    req = Request(url, method="GET")
    with urlopen(req, timeout=120.0) as resp:
        data = resp.read()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest


def run_txt2img_generation(
    *,
    base_url: str,
    workflow_template: dict[str, Any],
    client_id: str,
    prompt: str,
    filename_prefix: str,
    output_dir: Path,
    width: int,
    height: int,
    seed: int | None,
    poll_seconds: float,
    timeout_seconds: float,
    negative: str | None = None,
) -> Path | None:
    patched = patch_txt2img_workflow(
        workflow_template,
        prompt=prompt,
        filename_prefix=filename_prefix,
        output_dir=output_dir.resolve(),
        width=width,
        height=height,
        seed=seed,
        negative=negative,
    )
    prompt_id = queue_prompt(base_url, patched, client_id)
    wait_for_prompt(base_url, prompt_id, poll_seconds, timeout_seconds)
    return find_saved_image(output_dir, filename_prefix)


def run_edit_generation(
    *,
    base_url: str,
    workflow_template: dict[str, Any],
    client_id: str,
    prompt: str,
    reference_path: Path,
    output_dir: Path,
    output_name: str,
    seed: int | None,
    poll_seconds: float,
    timeout_seconds: float,
) -> Path | None:
    uploaded = upload_image(base_url, reference_path)
    patched = patch_edit_workflow(
        workflow_template,
        prompt=prompt,
        reference_image=uploaded,
        seed=seed,
    )
    prompt_id = queue_prompt(base_url, patched, client_id)
    history = wait_for_prompt(base_url, prompt_id, poll_seconds, timeout_seconds)
    images = extract_output_images(history)
    if not images:
        return None
    dest = output_dir / f"{output_name}.png"
    download_history_image(base_url, images[-1], dest)
    return dest
