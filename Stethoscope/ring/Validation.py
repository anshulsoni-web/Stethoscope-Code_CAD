import argparse
import os
import sys
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich import box
    _rich = True
    console = Console()
except ImportError:
    _rich = False

try:
    import trimesh
except ImportError:
    sys.exit("ERROR: trimesh not found.\nInstall it with:  pip install trimesh numpy\n")

SOURCE_KEYWORD = "source"
TOLERANCE_PCT  = 5


def is_source(path: Path) -> bool:
    return SOURCE_KEYWORD.lower() in path.stem.lower()


def discover_pair(directory: Path):
    all_stls = sorted(
        p for p in directory.iterdir()
        if p.is_file() and p.suffix.lower() == ".stl"
    )
    sources = [p for p in all_stls if is_source(p)]
    others  = [p for p in all_stls if not is_source(p)]

    if not sources:
        print(f"\nNo STL file containing '{SOURCE_KEYWORD}' found in: {directory}")
        if all_stls:
            print(f"Rename your reference file to include 'source', e.g.:  source_{all_stls[0].name}")
        return None

    if not others:
        print(f"\nOnly source file(s) found — no partner STL in: {directory}")
        print("Add your generated/output STL to this folder.")
        return None

    if len(sources) > 1:
        print(f"  ⚠  Multiple source files found — using first: {sources[0].name}")
    if len(others) > 1:
        print(f"  ⚠  Multiple non-source files found — using first: {others[0].name}")

    return (sources[0], others[0])


def mesh_volume(path: Path) -> float:
    mesh = trimesh.load_mesh(str(path), force="mesh")
    if not mesh.is_watertight:
        print(f"  ⚠  WARNING: '{path.name}' is not watertight — volume may be inaccurate.")
    return abs(float(mesh.volume))


def compare(src_path: Path, other_path: Path) -> dict:
    src_vol   = mesh_volume(src_path)
    other_vol = mesh_volume(other_path)
    diff      = other_vol - src_vol
    pct       = (diff / src_vol * 100) if src_vol else float("nan")
    return {
        "src":     src_path.name,
        "gen":     other_path.name,
        "src_vol": src_vol,
        "gen_vol": other_vol,
        "diff":    diff,
        "pct":     pct,
        "ok":      abs(pct) <= TOLERANCE_PCT,  # percentage only
    }


def _sign(v: float) -> str:
    return "+" if v >= 0 else ""


def print_plain(r: dict, directory: Path) -> None:
    sep    = "─" * 72
    status = "✓ MATCH" if r["ok"] else "✗ MISMATCH"
    print(f"\n{sep}")
    print(f"  STL Volumetric Comparison  —  {directory}")
    print(sep)
    print(f"\n  [{status}]")
    print(f"    Source    : {r['src']}")
    print(f"    Generated : {r['gen']}")
    print(f"    Src Vol   : {r['src_vol']:>16.4f} mm³")
    print(f"    Gen Vol   : {r['gen_vol']:>16.4f} mm³")
    print(f"    Difference: {_sign(r['diff'])}{r['diff']:>15.4f} mm³   ({_sign(r['pct'])}{r['pct']:.6f} %)")
    print(f"    Tolerance : ±{TOLERANCE_PCT}% (percentage only)")
    print(f"\n{sep}\n")


def print_rich_result(r: dict, directory: Path) -> None:
    ds  = "green" if r["ok"] else "red"
    sts = "[green]✓ MATCH[/green]" if r["ok"] else "[red]✗ MISMATCH[/red]"
    table = Table(
        title=f"STL Volumetric Comparison\n[dim]{directory}[/dim]",
        box=box.ROUNDED, show_lines=True, header_style="bold cyan",
    )
    table.add_column("File",         style="white", no_wrap=False)
    table.add_column("Role",         style="dim",   justify="center")
    table.add_column("Volume (mm³)", style="blue",  justify="right")
    table.add_column("Diff (mm³)",   justify="right")
    table.add_column("Diff (%)",     justify="right")
    table.add_column("Status",       justify="center")
    table.add_row(r["src"], "source",    f"{r['src_vol']:.4f}",
                  f"[{ds}]{_sign(r['diff'])}{r['diff']:.4f}[/{ds}]",
                  f"[{ds}]{_sign(r['pct'])}{r['pct']:.6f}[/{ds}]", sts)
    table.add_row(r["gen"], "generated", f"{r['gen_vol']:.4f}", "", "", "")
    console.print()
    console.print(table)
    console.print(f"  [dim]Tolerance: ±{TOLERANCE_PCT}% (percentage only)[/dim]")
    console.print()


def print_result(r: dict, directory: Path) -> None:
    if _rich:
        print_rich_result(r, directory)
    else:
        print_plain(r, directory)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Compare volumes of a source STL and its partner."
    )
    p.add_argument("stl_pair", nargs="*", metavar="STL",
                   help="Two STL paths to compare directly (source then generated).")
    p.add_argument("--dir", "-d", default=None, metavar="PATH",
                   help="Directory to scan (default: folder containing this script).")
    p.add_argument("--tolerance-pct", type=float, default=TOLERANCE_PCT, metavar="T",
                   help=f"Volume diff tolerance in %% (default: {TOLERANCE_PCT}).")
    p.add_argument("--list-pairs", action="store_true",
                   help="Preview discovered pair without computing volumes.")
    return p


def main() -> int:
    parser = build_parser()
    args   = parser.parse_args()

    global TOLERANCE_PCT
    TOLERANCE_PCT = args.tolerance_pct

    directory = (
        Path(args.dir).resolve() if args.dir
        else Path(os.path.abspath(__file__)).parent
    )
    if not directory.is_dir():
        sys.exit(f"ERROR: directory not found: {directory}")

    if args.stl_pair:
        if len(args.stl_pair) != 2:
            sys.exit("ERROR: provide exactly 2 STL paths.")
        src_path, other_path = Path(args.stl_pair[0]).resolve(), Path(args.stl_pair[1]).resolve()
        for p in (src_path, other_path):
            if not p.is_file():
                sys.exit(f"ERROR: file not found: {p}")
        pair = (src_path, other_path)
    else:
        pair = discover_pair(directory)

    if pair is None:
        return 1

    src_path, other_path = pair

    if args.list_pairs:
        print(f"\nPair found in {directory}:")
        print(f"  SOURCE    {src_path.name}")
        print(f"  GENERATED {other_path.name}\n")
        return 0

    print(f"  Computing: {src_path.name}  ↔  {other_path.name} …")
    try:
        result = compare(src_path, other_path)
    except Exception as exc:
        sys.exit(f"ERROR: {exc}")

    print_result(result, directory)
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())