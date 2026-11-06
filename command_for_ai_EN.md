# Technology Handbook Extraction Instructions for Codex

English (this file) · [中文](command_for_ai.md)

Every time you extract technologies from another project, first read this document, the [entry template](topics/TEMPLATE_EN.md) ([Chinese template](topics/TEMPLATE.md)) and the current indexes ([Chinese](README_CH.md), [English](README_EN.md)), and then carry out the task. The scope and phase that the user specifies explicitly for this run take priority over the default process.

## Goal and selection principles

Maintain a technology reference handbook, mainly in Chinese; pages added and updated from the 2025Codes round on also have an English version (see "Bilingual version rules" at the end), so that readers can quickly find "what it is, when to use it, how to use it, an example, and common problems". A project is only a clue for discovering technologies; do not produce a project retrospective, a directory translation, or a list of all dependencies.

- Prefer technologies that can be looked up independently: formats, protocols, libraries, SDKs, APIs, interface languages and concrete programming mechanisms, for example PCM, FIDL, Opus, MQTT, thread synchronization.
- Broad platforms or languages such as Linux and C/C++ do not get their own page; a concrete mechanism with independent value may be recorded.
- Finding third-party source, headers or a build dependency does not mean the project actually uses it. Check call sites, configuration and the build relationship, and distinguish actually used, merely bundled and cannot be confirmed.
- Search existing names, aliases and ecosystems, and prefer extending an existing page; technologies with the same name in different ecosystems must be told apart.
- Business-specific flows, duplicate projects, logs, build products and dependencies bundled inside an SDK usually do not become a page of their own. State the reason and the resume condition for deferred items, and do not generate entries just to make up numbers.

## Phase 1: Scan and candidate confirmation

1. Confirm the project path and scan scope the user gave, and read any repository instructions that apply. The source project is read-only: do not run unknown programs or build scripts, and do not connect to external services.
2. Use file search, build files and key call sites to locate candidate technologies. Look at handwritten source first, and skip version-control metadata, caches, binaries and duplicated third-party source.
3. For each item record the name, the specific purpose, the evidence of actual use, the existing page, the suggested handling and the uncertainty. Keep the evidence in the scan record, record only locators such as paths and symbols, do not copy old code, and do not leak credentials or private data.
4. By default summarize in the following six parts, consistent with the [confirmed list](catalog/2016-scope.md) (zh):
   - Audio processing.
   - Speech technology and SDKs.
   - Networking and data processing.
   - IoT communication.
   - Specific programming mechanisms.
   - Deferred, no standalone page.
5. Categories are for navigation only. For technologies in other fields, propose a suitable category and do not force them into existing ones; pages still all use the six-section template described below.
6. Give the lists of new, updated, merged and deferred items, with exact counts. By default a new project first submits a candidate summary and waits for the user to confirm before formal technology pages and examples are generated; when the user has clearly confirmed or authorized direct generation, continue without asking again.

During the scan phase, save the candidate record in `catalog/Chinese/<project short name>-scope.md` and `catalog/English/<project short name>-scope.md` (same content, different languages). If the user asks for "summary only, no files", show the result in the reply only and create no file.

## Phase 2: Choose the example source

New rule set by the user on 2026-10-26: the old-component reuse suggestions below are for historical judgment only and no longer authorize copying or referencing the old implementations. Teaching examples may only reuse code that this handbook has already written independently, or be newly written; all code references live inside DevelopingManual/examples. Formal technology pages do not reference historical project paths, and scan evidence stays only in catalog/ and the source audit.

Decide in the following order and record the approach actually taken:

1. Check the independent teaching examples the handbook already has, and look at the [source notes](catalog/English/sources.md) ([Chinese original](catalog/Chinese/sources.md)) to verify their origin; old components are for historical audit only, and the old repository structure is not restored or their implementation copied.
2. Before reusing a handbook example, check its independent origin, actual function, interface and dependencies, input boundaries, resource release and license. A similar file name is not a basis for reuse.
3. If it applies, reuse it, correcting it where needed and stating the change; if it does not apply or cannot be obtained, write a new, independent, minimal, runnable teaching example.
4. **Never copy, rename-and-move, or reference code from the scanned old project as a handbook example.** Keep scan evidence and teaching code apart: the body text uses official material and the handbook's own examples, and the historical project is used only to identify technologies.
5. Do not describe a mock, a hard-coded result or a simple placeholder function as a real integration. Without a vendor SDK, authorization or accurate documentation, provide only a clearly labeled integration contract or syntax sketch, and list what is missing to complete the integration.

Examples must be independent of the source project directory and must not carry old binaries, models, accounts, private service addresses or a whole third-party SDK.

## Phase 3: Write the technology pages

Each formal entry is written in the following six sections according to [TEMPLATE_EN.md](topics/TEMPLATE_EN.md); the six sections here are the page structure and differ from the six-part categories of the candidate list:

1. **What it is**: the accurate concept, key characteristics, and the relationship to related technologies.
2. **When to use**: suitable scenarios, constraints and limits.
3. **How to use**: dependencies, version/platform, configuration, steps, inputs and outputs, and resource lifecycle.
4. **Minimal example**: link into `examples/`, and give the command run from the handbook root, the expected result and the verification status.
5. **FAQ**: boundary conditions, error handling and troubleshooting related to the technology.
6. **References**: prefer the official documentation or standard for the matching version, and link related entries.

The top of the page lists the name/aliases, ecosystem, applicable versions and platforms, tags, example status and code source. State explicitly any version or interface that cannot be confirmed; do not invent information and do not treat a historical interface as the current one by default.

The body is centered on lookup and use and avoids pasting source repeatedly. Short necessary snippets may be shown, and complete examples are kept in `examples/`. Use links across topics and do not copy whole pages.

## Phase 4: Verification and delivery

- Run suitable checks on examples that can be verified locally, preferring offline data, local loopback services and temporary output directories; test real boundaries and failure paths, and avoid tests that merely restate the implementation.
- Run `make test` according to what changed, and `make test-media` when media codecs are involved. Wire new entries into the check script when needed, and do not install full SDKs for unrelated documentation changes.
- Record these separately: run and verified, compiled only, unverified (missing dependency/device/service), and syntax sketch or integration contract. Record the actual environment and never write an expected result as an executed result.
- FFmpeg verification cannot replace compiling an example for a specific C library; offline tests cannot prove that a real device, cloud service, broker or proprietary SDK has been integrated successfully.
- Do not automatically send cloud requests, publish MQTT messages, write to hardware, or run other demos with external effects; follow the scope the user has authorized for integration.
- Check page structure, local links, Python syntax and `git diff --check`. If a dependency is missing, say so explicitly and do not fake a pass record.
- Update the navigation of `README_CH.md` and `README_EN.md`, the verification scope of `examples/README.md`, and the reuse decisions in `catalog/Chinese/sources.md`. Keep the records of other projects and do not overwrite them into documents that describe only this round's task.
- A README only does navigation: add the new pages to the matching language/framework tables, update the total page count, and add one line in the scan list at the top that links to the scan record. **Do not add a section such as "XXXXCodes scan results/summary" to a README.** Scan results, counts, and done and pending status are written only in the scan records under `catalog/Chinese/` and `catalog/English/`; the check script rejects a README section whose heading contains `XXXXCodes`.
- Finally, report briefly in Chinese the entries added/updated, what was reused and what was newly written, the actual check results, and the items still awaiting integration. Do not commit, push or publish automatically unless asked.

## Repository management

Documentation and teaching examples are kept together in this repository, with categories expressed by directories and indexes. Consider a separate repository only for a component that needs independent building, publishing and reuse; consider a submodule only when the build really depends on another source repository. Do not create a sub-repository for every technology.

These instructions do not authorize deleting other projects, sub-repositories or user files, nor restoring the old structure that was cleaned up earlier. When cleanup is involved, handle it according to the explicit scope of this run and protect existing uncommitted changes.

## Instruction template for each use

Replace the paths and scope in the following and give it to Codex:

```text
Please first read DevelopingManual/command_for_ai_EN.md and follow the process in it.

Handbook repository: <absolute path of DevelopingManual>
Projects to scan: <absolute project path, several allowed>
Scan scope for this run: <the whole project or specific directories/modules>

First scan and summarize the technologies worth putting into the handbook,
distinguishing new, updated, merged and deferred items, and give the evidence
of actual use and suggestions for the example source. Do not generate formal
technology pages or code in this phase; wait until I confirm the list.

After confirmation: do not reference or copy old project code; first check the
independent teaching examples the handbook already has, reuse them where they
fit, and otherwise write new ones. All teaching code goes in DevelopingManual/examples.
Every formal entry uses the prescribed six-section structure, and the indexes,
source notes and verification status are updated.
```

If the scope has already been confirmed, replace "First scan ... wait until I confirm the list" with "The following list is confirmed; complete the writing and verification directly: <list>", and there is no need to confirm the same scope again.

## Bilingual version rules (added 2026-11-06)

The user's requirement: the Markdown files produced by the process each get a Chinese and an English version, with the same content in different languages.

- These instructions: `command_for_ai.md` is the Chinese version and `command_for_ai_EN.md` is the English version; their sections and rules correspond one to one, and changing one requires changing the other in step.
- Indexes: `README_CH.md` (Chinese) and `README_EN.md` (English), with the same structure; the rule is in Phase 4 above: a README holds no scan-results section. The English version of `examples/README.md` is `examples/README_EN.md`.
- Scan records: `catalog/Chinese/<project short name>-scope.md` and `catalog/English/<project short name>-scope.md`, linked to each other, with the numbers and evidence necessarily consistent. Records from before 2025Codes stay at the `catalog/` root, in Chinese only, and are not migrated.
- Source notes: `catalog/Chinese/sources.md` and `catalog/English/sources.md`; no sources file is kept in the repository root.
- New technology pages: `topics/Chinese/<category>/<name>.md` and `topics/English/<category>/<name>.md`. The Chinese page uses the six section headings of the [template](topics/TEMPLATE.md); the English page uses What it is / When to use / How to use / Minimal example / FAQ / References from the [English template](topics/TEMPLATE_EN.md).
- Updating a page from before 2025Codes: edit the Chinese page in place; the English version is a full-page translation placed in the same-named file under `topics/English/<category>/`. The other pages that have not been updated have no English version for now.
- Teaching code exists once, in `examples/`, and is not split by language.
- `tools/check_handbook.py` checks English page headings, one-to-one pairing of Chinese and English pages, the pairing of the two language directories under `catalog/`, the matching structure of the two READMEs, and the matching structure of these two instruction files. Both languages must pass it before delivery.
