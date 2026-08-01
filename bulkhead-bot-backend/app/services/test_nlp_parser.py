import importlib
import sys
import types

import pytest


def _load_parser_module():
    google_module = types.ModuleType("google")
    genai_module = types.ModuleType("google.genai")

    class _FakeClient:
        def __init__(self, *args, **kwargs):
            self.models = types.SimpleNamespace(generate_content=lambda *a, **k: None)

    genai_module.Client = _FakeClient
    google_module.genai = genai_module

    dotenv_module = types.ModuleType("dotenv")
    dotenv_module.load_dotenv = lambda *args, **kwargs: None

    original_modules = {
        name: sys.modules.get(name)
        for name in ("google", "google.genai", "dotenv")
    }

    sys.modules["google"] = google_module
    sys.modules["google.genai"] = genai_module
    sys.modules["dotenv"] = dotenv_module

    try:
        module_name = "app.services.nlp_parser"
        if module_name in sys.modules:
            del sys.modules[module_name]
        return importlib.import_module(module_name)
    finally:
        for name, module in original_modules.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


nlp_parser = _load_parser_module()


def test_hardcoded_exact_months():
    assert nlp_parser.normalize_timeline_to_months_hardcoded("7 months") == 7.0


def test_hardcoded_decimal_months():
    assert nlp_parser.normalize_timeline_to_months_hardcoded("2.5 months") == 2.5


def test_hardcoded_weeks_to_months():
    assert nlp_parser.normalize_timeline_to_months_hardcoded("2 to 3 weeks") == 0.6


def test_hardcoded_asap():
    assert nlp_parser.normalize_timeline_to_months_hardcoded("ASAP") == 0.0


def test_main_uses_hardcoded_first(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("Gemini should not be called for simple inputs")

    monkeypatch.setattr(nlp_parser.client.models, "generate_content", fail_if_called)

    assert nlp_parser.normalize_timeline_to_months("7 months") == 7.0


def test_main_falls_back_to_gemini_when_hardcoded_returns_none(monkeypatch):
    monkeypatch.setattr(
        nlp_parser,
        "normalize_timeline_to_months_hardcoded",
        lambda raw: None,
    )

    class FakeResponse:
        text = "4.0"

    monkeypatch.setattr(
        nlp_parser.client.models,
        "generate_content",
        lambda *args, **kwargs: FakeResponse(),
    )

    assert nlp_parser.normalize_timeline_to_months("sometime soon") == 4.0


def test_blank_input_returns_safe_default():
    assert nlp_parser.normalize_timeline_to_months("") == 99.0