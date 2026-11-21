"""Self-check of the product-doc parser on a tiny fixture: python3 scripts/test_generate.py"""

import generate as g

HTML = (
    "<h2>4. Decyzje architektoniczne (ADR)</h2><p>Wstęp z ADR-01.</p>"
    "<h3>ADR-01. Pierwsza</h3><table><tbody><tr><td>Status</td><td><strong>Przyjęta</strong></td></tr>"
    "<tr><td>Decyzja</td><td>Patrz ADR-02 i ADR-99, pole <span style=\"font-family:'Azeret Mono'\">a|b</span>.</td></tr></tbody></table>"
    "<h3>ADR-02. Druga</h3><table><tbody><tr><td>Status</td><td>Proponowana</td></tr></tbody></table>"
    "<h2>8. Słownik pojęć</h2><table><thead><tr><th>Pojęcie</th><th>Znaczenie</th></tr></thead>"
    "<tbody><tr><td><strong>Werdykt</strong></td><td>Ocena, zob. ADR-01.</td></tr></tbody></table>"
)

if __name__ == "__main__":
    import tempfile
    from pathlib import Path

    g.DOCS = Path(tempfile.mkdtemp())
    g.write_product_doc(HTML)
    adr1 = (g.DOCS / "adr" / "adr-01.md").read_text()
    assert "**Status:** Przyjęta" in adr1, adr1
    assert "[ADR-02](adr-02.md)" in adr1 and "ADR-99" in adr1 and "[ADR-99]" not in adr1, adr1
    assert "`a\\|b`" in adr1, adr1
    index = (g.DOCS / "adr" / "index.md").read_text()
    assert "[ADR-01](adr-01.md)" in index and "| Proponowana |" in index, index
    glossary = (g.DOCS / "slownik.md").read_text()
    assert "Werdykt\n:   Ocena, zob. [ADR-01](adr/adr-01.md)." in glossary, glossary
    print("ok")
