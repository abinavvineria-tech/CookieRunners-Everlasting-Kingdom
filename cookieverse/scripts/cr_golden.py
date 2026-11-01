#!/usr/bin/env python3
"""
cr-golden CLI companion for Cookie Runners Golden Ballon d'Or 2026.
Usage:
  cr-golden ceremony   - Show ceremony info
  cr-golden winners    - List winners
  cr-golden awards     - List award categories
  cr-golden history    - Show ceremony history
  cr-golden nominees   - List nominees
  cr-golden version    - Show version
"""
import click
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_all_categories, get_all_winners, get_nominees, get_moments

@click.group()
@click.version_option(version="1.0.0", prog_name="cr-golden")
def cli():
    """Cookie Runners Golden Ballon d'Or — CLI Companion."""
    pass

@cli.command()
def ceremony():
    """Show the first edition ceremony details."""
    click.echo("Cookie Runners Golden Ballon d'Or — First Edition 2026")
    click.echo("Tagline: Every Cookie. Every Legend. One Golden Legacy.")
    click.echo("Motto: United by Cookies. Remembered by Legends.")
    click.echo("Golden Ballon d'Or: White Lily Cookie, Mogra Cookie")
    click.echo("Golden Heart Award: White Lily Cookie, Mogra Cookie")
    click.echo("Golden Teammate Award: Pure Vanilla Cookie")

@cli.command()
def winners():
    """List all award winners."""
    winners = get_all_winners()
    if not winners:
        click.echo("No winners found.")
        return
    click.echo(f"{'Category':<30} {'Name':<25} {'Role':<30} {'Year'}")
    click.echo("-" * 100)
    for w in winners:
        click.echo(f"{w.get('category_name',''):<30} {w.get('name',''):<25} {w.get('role_text',''):<30} {w.get('year','')}")

@cli.command()
def awards():
    """List award categories."""
    cats = get_all_categories()
    click.echo(f"{'Category':<30} {'Slug'}")
    click.echo("-" * 60)
    for c in cats:
        click.echo(f"{c['name']:<30} {c['slug']}")

@cli.command()
def history():
    """Show ceremony history (moments and editions)."""
    moments = get_moments()
    click.echo("Golden Moments:")
    for m in moments:
        click.echo(f"  {m['year']} — {m['title']}: {m['description']}")

@cli.command()
def nominees():
    """List current nominees."""
    noms = get_nominees()
    if not noms:
        click.echo("No nominees yet.")
        return
    click.echo(f"{'Name':<25} {'Category ID':<15} {'Year':<6} {'By'}")
    click.echo("-" * 70)
    for n in noms:
        click.echo(f"{n['name']:<25} {str(n['category_id']):<15} {str(n['year']):<6} {n.get('nominated_by','')}")

@cli.command()
def version():
    """Show CLI version."""
    click.echo("cr-golden version 1.0.0 — Cookie Runners Golden Ballon d'Or 2026")

if __name__ == "__main__":
    cli()
