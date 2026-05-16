"""docparse CLI — extract structured data from documents."""
from __future__ import annotations
import json
import sys
import click
from .loader    import load
from .extractor import LLMExtractor
from .schemas   import REGISTRY
from .models    import ExtractionSchema, FieldSpec


@click.group()
def cli():
    """docparse — LLM-powered document extraction."""


@cli.command()
@click.option("--file",   "-f", required=True, help="Path to document (PDF, TXT)")
@click.option("--schema", "-s", required=True, help=f"Schema name: {', '.join(REGISTRY)} — or path to JSON schema file")
@click.option("--model",  "-m", default="gpt-4o-mini", help="LLM model (default gpt-4o-mini)")
@click.option("--provider", "-p", default="openai", help="LLM provider: openai | anthropic")
@click.option("--output", "-o", default="json", type=click.Choice(["json", "table"]))
def extract(file, schema, model, provider, output):
    """Extract structured data from a document."""
    layout = load(file)

    if schema in REGISTRY:
        sch = REGISTRY[schema]
    else:
        try:
            raw = json.loads(open(schema).read())
            sch = ExtractionSchema(
                name=raw.get("name", "custom"),
                fields=[FieldSpec(**f) for f in raw["fields"]],
            )
        except Exception as e:
            raise click.BadParameter(f"Could not load schema: {e}")

    extractor = LLMExtractor(model=model, provider=provider)
    result    = extractor.extract(layout, sch)

    if output == "json":
        click.echo(json.dumps({
            k: {"value": v.value, "confidence": round(v.confidence, 2)}
            for k, v in result.fields.items()
        }, indent=2))
    else:
        click.echo(f"{'Field':<25} {'Value':<40} {'Confidence':>10}")
        click.echo("-" * 78)
        for k, v in result.fields.items():
            val = str(v.value) if v.value is not None else "(not found)"
            click.echo(f"{k:<25} {val:<40} {v.confidence:>10.0%}")

    missing = result.missing_required(sch)
    if missing:
        click.echo(f"\n⚠ Missing required fields: {', '.join(missing)}", err=True)
        sys.exit(1)


@cli.command()
def schemas():
    """List available built-in schemas."""
    for name, sch in REGISTRY.items():
        click.echo(f"{name:<20} ({len(sch.fields)} fields)")


def main():
    cli()
