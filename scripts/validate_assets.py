#!/usr/bin/env python3
"""Offline APK asset kontrolü.

Bu script GitHub Actions içinde JSON dosyalarının okunabildiğini, standart kodlarının
çakışmadığını ve görsel asset yollarının repo içinde bulunup bulunmadığını kontrol eder.
Eksik görseller varsayılan olarak uyarıdır; çünkü görsel dosyaları sonradan yüklenebilir.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

STANDARD_FILES = [
    ROOT / "assets" / "standards.json",
    ROOT / "assets" / "standards_extra.json",
]
EDUCATION_FILES = [
    ROOT / "assets" / "education_notes.json",
    ROOT / "assets" / "education_notes_extra.json",
]
VISUAL_FILES = [
    ROOT / "assets" / "visual_notes.json",
    ROOT / "assets" / "visual_notes_extra.json",
]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"HATA: Dosya bulunamadı: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"HATA: JSON okunamadı: {path.relative_to(ROOT)} -> {exc}")


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def as_map(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict-images", action="store_true", help="Eksik imageAsset dosyalarında hata ver.")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    standards: list[dict[str, Any]] = []
    for path in STANDARD_FILES:
        data = load_json(path)
        if not isinstance(data, list):
            errors.append(f"{path.relative_to(ROOT)} liste olmalı.")
            continue
        standards.extend([item for item in data if isinstance(item, dict)])

    codes = [str(item.get("code", "")).strip() for item in standards]
    empty_codes = [item.get("title", "<başlıksız>") for item in standards if not str(item.get("code", "")).strip()]
    for title in empty_codes:
        errors.append(f"Standart code boş: {title}")

    duplicate_codes = [code for code, count in Counter(codes).items() if code and count > 1]
    for code in duplicate_codes:
        warnings.append(f"Tekrarlı standart code: {code}")

    standard_key_set = {str(item.get("code", "")).strip() for item in standards}
    standard_key_set.update(str(item.get("title", "")).strip() for item in standards)

    education_map: dict[str, Any] = {}
    for path in EDUCATION_FILES:
        data = load_json(path)
        if not isinstance(data, dict):
            errors.append(f"{path.relative_to(ROOT)} nesne/dict olmalı.")
            continue
        education_map.update(data)

    for key in education_map:
        if key not in standard_key_set:
            warnings.append(f"Eğitim notu anahtarı standartlarda bulunamadı: {key}")

    visual_count = 0
    missing_assets: list[str] = []
    for path in VISUAL_FILES:
        data = load_json(path)
        if not isinstance(data, list):
            errors.append(f"{path.relative_to(ROOT)} liste olmalı.")
            continue
        for entry in data:
            if not isinstance(entry, dict):
                warnings.append(f"{path.relative_to(ROOT)} içinde görsel kaydı dict değil.")
                continue
            visual_count += 1
            standards_for_visual = entry.get("standards", [])
            if not isinstance(standards_for_visual, list) or not standards_for_visual:
                warnings.append(f"Görsel standards alanı boş: {entry.get('title', '<başlıksız>')}")
            for key in standards_for_visual if isinstance(standards_for_visual, list) else []:
                if str(key).strip() not in standard_key_set:
                    warnings.append(f"Görsel standard anahtarı standartlarda bulunamadı: {key}")
            image_asset = str(entry.get("imageAsset", "")).strip()
            image_base64 = str(entry.get("imageBase64", "")).strip()
            if image_asset:
                asset_path = ROOT / image_asset
                if not asset_path.exists():
                    missing_assets.append(image_asset)
            elif not image_base64:
                warnings.append(f"Görsel kaydında imageAsset veya imageBase64 yok: {entry.get('title', '<başlıksız>')}")

    if missing_assets:
        msg = "Eksik imageAsset dosyaları: " + ", ".join(missing_assets[:30])
        if args.strict_images:
            errors.append(msg)
        else:
            warnings.append(msg)

    print("--- Offline APK asset kontrolü ---")
    print(f"Standart sayısı: {len(standards)}")
    print(f"Eğitim notu anahtarı: {len(education_map)}")
    print(f"Görsel notu sayısı: {visual_count}")
    print(f"Eksik görsel asset: {len(missing_assets)}")

    if warnings:
        print("\nUYARILAR:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("\nHATALAR:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("\nKontrol tamamlandı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
