"""The digest check over OCI image manifests and indexes.

The fixture under ``fixtures/gemara-bundle`` is ``testdata/minimal-catalog.yaml`` from
gemaraproj/gemara-publish-action at commit 7ef3743 (Apache-2.0) and the OCI image manifest a
local ``registry:2`` returned for it after that commit's ``grc`` pushed it, read back with
``oras manifest fetch``. The manifest's one layer digest is the SHA-256 of the YAML file.
"""

import hashlib
import json
from pathlib import Path

import pytest
from agent_evidence_admission import digest_check
from agent_evidence_admission.cli import main

FIXTURE = Path(__file__).parent / "fixtures" / "gemara-bundle"
LAYER = b"kind: Catalog\n"
CONFIG = b'{"bundle-version":"1"}'
OTHER = b"some other bytes\n"


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def manifest(*layers: bytes, config: bytes | None = CONFIG, subject: bytes | None = None) -> dict:
    document: dict = {
        "schemaVersion": 2,
        "mediaType": "application/vnd.oci.image.manifest.v1+json",
        "layers": [{"mediaType": "application/octet-stream", "digest": sha256(b), "size": len(b)} for b in layers],
    }
    if config is not None:
        document["config"] = {"mediaType": "application/vnd.oci.empty.v1+json", "digest": sha256(config)}
    if subject is not None:
        document["subject"] = {"mediaType": "application/vnd.oci.image.manifest.v1+json", "digest": sha256(subject)}
    return document


CASES = [
    # (name, document, artifact, ok, reason)
    ("layer named", manifest(OTHER, LAYER), LAYER, True, ""),
    ("config named", manifest(OTHER), CONFIG, True, ""),
    ("bytes differ from every layer", manifest(LAYER), OTHER, False, "digest-mismatch"),
    ("layer missing from the manifest", manifest(OTHER), LAYER, False, "digest-mismatch"),
    ("manifest names no content", manifest(config=None), LAYER, False, "no-digest-named"),
    ("subject is not content", manifest(config=None, subject=LAYER), LAYER, False, "no-digest-named"),
]


@pytest.mark.parametrize(("name", "document", "artifact", "ok", "reason"), CASES, ids=[c[0] for c in CASES])
def test_manifest_cases(name, document, artifact, ok, reason):
    result = digest_check.check(document, artifact)
    assert (result.ok, result.reason) == (ok, reason), name


def test_the_cases_are_not_answered_by_a_constant_verdict():
    # A checker that passes everything, or fails everything, gets some of these wrong.
    verdicts = {ok for _, _, _, ok, _ in CASES}
    assert verdicts == {True, False}
    for constant in (True, False):
        assert any(ok != constant for _, _, _, ok, _ in CASES)


def test_an_index_names_its_manifests():
    child = json.dumps(manifest(LAYER)).encode()
    index = {
        "schemaVersion": 2,
        "mediaType": "application/vnd.oci.image.index.v1+json",
        "manifests": [{"mediaType": "application/vnd.oci.image.manifest.v1+json", "digest": sha256(child)}],
    }
    assert digest_check.check(index, child).ok
    assert digest_check.check(index, LAYER).reason == "digest-mismatch"


def test_a_manifest_without_media_type_is_read_by_its_shape():
    document = manifest(LAYER)
    del document["mediaType"]
    assert digest_check.check(document, LAYER).ok


def test_sha512_and_malformed_descriptors():
    document = {
        "schemaVersion": 2,
        "layers": [
            {"digest": "sha512:" + hashlib.sha512(LAYER).hexdigest()},
            {"digest": "no-colon"},
            {"digest": "md5:abc"},
            {"digest": 7},
            "not a descriptor",
        ],
    }
    assert digest_check.declared_digests(document) == [("sha512", hashlib.sha512(LAYER).hexdigest())]
    assert digest_check.check(document, LAYER).ok


def test_gemara_bundle_layer_is_the_source_file(capsys):
    manifest_path, catalog = FIXTURE / "manifest.json", FIXTURE / "minimal-catalog.yaml"
    assert main(["digest-check", str(manifest_path), str(catalog)]) == 0
    out = capsys.readouterr().out
    assert out.startswith("PASS ") and "sha256:ec84448608b81dc12bccc964d5b1359f3151107609a1a03bc1f0b89575fcf9e1" in out


def test_gemara_bundle_refuses_an_edited_catalog(tmp_path, capsys):
    edited = tmp_path / "minimal-catalog.yaml"
    edited.write_bytes((FIXTURE / "minimal-catalog.yaml").read_bytes() + b"# edited\n")
    assert main(["digest-check", str(FIXTURE / "manifest.json"), str(edited)]) == 1
    assert capsys.readouterr().out.startswith("FAIL digest-mismatch")
