"""Generate a simple signed PDF report (reference implementation).

Intended output:
- a PDF artifact
- a JSON sidecar with provenance fields (commit, signer, backend, mitigation)
- optional: record in ledger

This demo uses reportlab to generate PDFs.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

@dataclass
class Provenance:
    commit: str
    signer: str
    backend: str
    provider: str
    mitigation: list[str]
    created_utc: str

def write_report(out_pdf: Path, prov: Provenance, title: str, body_lines: list[str]) -> None:
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out_pdf), pagesize=letter)
    width, height = letter

    y = height - 72
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, y, title)
    y -= 28

    c.setFont("Helvetica", 10)
    c.drawString(72, y, f"commit: {prov.commit}")
    y -= 14
    c.drawString(72, y, f"signer: {prov.signer}")
    y -= 14
    c.drawString(72, y, f"provider/backend: {prov.provider}/{prov.backend}")
    y -= 14
    c.drawString(72, y, f"mitigation: {', '.join(prov.mitigation) if prov.mitigation else 'none'}")
    y -= 22

    c.setFont("Helvetica", 11)
    for line in body_lines:
        if y < 72:
            c.showPage()
            y = height - 72
            c.setFont("Helvetica", 11)
        c.drawString(72, y, line)
        y -= 14

    c.showPage()
    c.save()

    # JSON sidecar
    sidecar = out_pdf.with_suffix(".json")
    sidecar.write_text(json.dumps(asdict(prov), indent=2), encoding="utf-8")

if __name__ == "__main__":
    # Example usage
    out = Path("epi_artifacts/demo_report.pdf")
    prov = Provenance(commit="(unknown)", signer="(unknown)", backend="aer", provider="qiskit",
                      mitigation=["m3","zne"], created_utc=datetime.utcnow().isoformat()+"Z")
    write_report(out, prov, "Epi‑Onto‑Learning Demo Report", ["Hello from the reference publisher."])
