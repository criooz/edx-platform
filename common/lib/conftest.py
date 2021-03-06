"""Code run by pylint before running any tests."""  # lint-amnesty, pylint: disable=django-not-configured

# Patch the xml libs before anything else.


import pytest

from safe_lxml import defuse_xml_libs

defuse_xml_libs()


@pytest.fixture(autouse=True)
def no_webpack_loader(monkeypatch):  # lint-amnesty, pylint: disable=missing-function-docstring
    monkeypatch.setattr(
        "webpack_loader.templatetags.webpack_loader.render_bundle",
        lambda entry, extension=None, config='DEFAULT', attrs='': ''
    )
    monkeypatch.setattr(
        "webpack_loader.utils.get_as_tags",
        lambda entry, extension=None, config='DEFAULT', attrs='': []
    )
    monkeypatch.setattr(
        "webpack_loader.utils.get_files",
        lambda entry, extension=None, config='DEFAULT', attrs='': []
    )
