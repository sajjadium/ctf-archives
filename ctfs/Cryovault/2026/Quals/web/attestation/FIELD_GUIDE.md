# Cryovault Attestation — field guide

The Winter Intake team moved its custody records to a small OCI-inspired registry. A notary can seal a retired case manifest. Review grants a ticket for an image index; the opening desk accepts that ticket and an index reference. The opening desk should never release a live case without valid review, a release layer, and a signed claim associated with the selected child.

Each case session is a writable, isolated copy of repository `cryovault`. The starting tag is named in the session's catalog at `/catalog.json`; machine-readable intake requirements are at `/policy.json`. The registry holds objects addressed by their SHA-256 digest. Requests and errors are JSON, except object downloads, which return the original bytes. This service models only the routes listed here; it is not a general OCI registry.

## Your case session

The address on the challenge page is a front desk shared by every team. Open a case session there (**Open a case file**), or from a script send `POST /session` with `Accept: application/json`; the answer is `{"token": ..., "base": ...}`. Every route in this guide lives under your session base: `/catalog.json` means `<base>/catalog.json`, `/v2/cryovault/tags/list` means `<base>/v2/cryovault/tags/list`, and so on. Nobody else sees what you write to your session, and anyone holding its base works in it. A session closes after about three hours unused; a new session is a new case.

## Registry

- `GET /v2/cryovault/tags/list`
- `GET /v2/cryovault/manifests/{tag-or-digest}`
- `PUT /v2/cryovault/manifests/{tag-or-digest}` with `Content-Type: application/vnd.oci.image.manifest.v1+json` or `application/vnd.oci.image.index.v1+json`
- `GET /v2/cryovault/blobs/{digest}`
- `PUT /v2/cryovault/blobs/{digest}` with a JSON config, JSON evidence, or POSIX tar layer. See `/policy.json` for media types and release path.
- `GET /v2/cryovault/referrers/{manifest-digest}`

Digest syntax is `sha256:` followed by 64 lowercase hex digits. A descriptor contains `mediaType`, `digest`, and raw byte `size`; index manifest descriptors also contain a `platform` with `os` and `architecture`. Uploaded manifests must reference objects already in the registry. Use raw bytes for hashing and sizing, since reformatting JSON changes a digest.

The registry supports a legacy referrers mode described in the OCI distribution specification.

## Custody desks

- `POST /api/notarize` with `{"digest":"sha256:..."}` returns a notary referrer for a retired image manifest associated with the catalog case.
- `POST /api/review` with `{"reference":"tag-or-digest"}` returns the selected child and a ticket for an index that satisfies review.
- `POST /api/open` with `{"reference":"tag-or-digest","ticket":"..."}` opens the reviewed index.

You can inspect the registry from the web interface. The underlying format references are the [OCI image index](https://github.com/opencontainers/image-spec/blob/main/image-index.md), [OCI image manifest](https://github.com/opencontainers/image-spec/blob/main/manifest.md), and [OCI distribution specification](https://github.com/opencontainers/distribution-spec/blob/main/spec.md). The challenge service intentionally implements a narrow subset of these formats.

The event flag uses the `isfcr` prefix.
