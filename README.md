# PolicyGuard – LLM-Powered Moderation System

An LLM-powered, rule-enhanced moderation system for scalable text-processing pipelines. This tool uses the OpenAI API, custom rule-based filters, and a JSON Schema for policy definition to create a powerful and auditable moderation workflow.

## Features

- **Hybrid Moderation:** Combines the nuance of Large Language Models with the precision of rule-based filters (Regex, keyword sets).
- **Structured Policies:** Define moderation policies using a modular and clear JSON Schema.
- **Batch Processing:** A command-line interface (CLI) designed to validate thousands of records from a file.
- **Audit Trail:** Flagged outputs are stored in a structured format to support human review and compliance audits.

## Getting Started

### Prerequisites
- Python 3.8+
- An OpenAI API Key

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/allen6711/policy-guard.git](https://github.com/allen6711/policy-guard.git)
   cd policy-guard