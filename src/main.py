import os
import click
import pandas as pd
from tqdm import tqdm
from datetime import datetime

# --- START OF FIX ---
# Load environment variables FIRST, before importing our own modules
from dotenv import load_dotenv
load_dotenv()

# THEN, import our modules that depend on those environment variables
from src.policy_loader import load_and_validate_policy, PolicyError
from src.core_engine import moderate_text
# --- END OF FIX ---

@click.group()
def cli():
    """
    PolicyGuard: An LLM-powered moderation tool.
    """
    pass

# --- COMMAND 1: PROCESS ---
@cli.command()
@click.option('--input-file', '-i', required=True, type=click.Path(exists=True, dir_okay=False), help='Path to the input CSV file.')
@click.option('--output-file', '-o', type=click.Path(dir_okay=False), help='Path to save the output CSV file. [Optional]')
@click.option('--policy', '-p', required=True, type=click.Path(exists=True, dir_okay=False), help='Path to the moderation policy file.')
@click.option('--text-column', '-c', required=True, type=str, help='The name of the column containing the text to moderate.')
def process(input_file, output_file, policy, text_column):
    """
    Process a CSV file against a moderation policy and save the results.
    """
    click.echo("🚀 Initializing PolicyGuard...")

    # This check is now slightly redundant but good to keep as a safeguard
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        click.secho("Error: OPENAI_API_KEY could not be loaded.", fg='red')
        return
    click.secho("✅ OpenAI API key loaded.", fg='green')

    try:
        loaded_policy = load_and_validate_policy(policy)
        click.secho(f"✅ Policy '{loaded_policy['name']}' loaded and validated.", fg='green')
    except PolicyError as e:
        click.secho(f"Error loading policy: {e}", fg='red')
        return

    click.echo("-----------------------------------------")

    try:
        df = pd.read_csv(input_file)
        if text_column not in df.columns:
            click.secho(f"Error: Text column '{text_column}' not found in the input file.", fg='red')
            return
        click.secho(f"✅ Input file '{input_file}' loaded. Found {len(df)} records.", fg='green')
    except Exception as e:
        click.secho(f"Error reading CSV file: {e}", fg='red')
        return

    results = []
    click.echo("⏳ Starting moderation process...")

    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Moderating"):
        text_to_check = str(row[text_column])

        if pd.isna(text_to_check) or not text_to_check.strip():
            result = {'flagged': False, 'reason': 'empty_text', 'details': ''}
        else:
            result = moderate_text(text_to_check, loaded_policy)

        output_row = row.to_dict()
        output_row.update(result)
        results.append(output_row)

    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(input_file).replace('.csv', '')
        output_file = os.path.join('output', f"{base_name}_results_{timestamp}.csv")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)

    click.secho(f"✅ Processing complete. Results saved to '{output_file}'", fg='green')

# --- COMMAND 2: REVIEW ---
@cli.command()
@click.option('--input-file', '-i', required=True, type=click.Path(exists=True, dir_okay=False), help='Path to the results CSV file from the "process" command.')
@click.option('--output-file', '-o', required=True, type=click.Path(dir_okay=False), help='Path to save the filtered review sheet.')
def review(input_file, output_file):
    """
    Generate a review sheet with only the flagged items.
    """
    click.echo("📄 Generating review sheet...")
    try:
        df = pd.read_csv(input_file)

        if 'flagged' not in df.columns:
            click.secho(f"Error: 'flagged' column not found in '{input_file}'. Please provide a valid results file.", fg='red')
            return

        flagged_df = df[df['flagged'] == True].copy()

        if flagged_df.empty:
            click.secho("✨ No flagged items found. No review sheet generated.", fg='green')
            return

        flagged_df['reviewer_decision'] = ''
        flagged_df['reviewer_comments'] = ''

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        flagged_df.to_csv(output_file, index=False)

        click.secho(f"✅ Review sheet generated with {len(flagged_df)} flagged items. Saved to '{output_file}'", fg='green')

    except Exception as e:
        click.secho(f"An error occurred: {e}", fg='red')


if __name__ == '__main__':
    cli()