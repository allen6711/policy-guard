import os
import click
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@click.group()
def cli():
    """
    PolicyGuard: An LLM-powered moderation tool.
    """
    pass

@cli.command()
@click.option('--file', '-f', required=True, type=click.Path(exists=True), help='Path to the data file to process.')
def process(file):
    """
    Process a file against a moderation policy.
    """
    click.echo("🚀 Initializing PolicyGuard...")

    # 1. Verify API Key is loaded
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        click.secho("Error: OPENAI_API_KEY not found in .env file.", fg='red')
        return

    click.secho("✅ OpenAI API key loaded successfully.", fg='green')
    click.echo(f"Processing file: {file}")
    click.echo("-----------------------------------------")
    # In future parts, we will add the core logic here.
    click.echo("🚧 Part 1 setup complete. Core logic will be added in the next steps.")


if __name__ == '__main__':
    cli()