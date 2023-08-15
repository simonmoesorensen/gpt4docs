# GPT4Docs: Documentation Generation with ChatGPT

## Description

GPT-4Docs is a Python project that utilizes the GPT-4 model for generating comprehensive documentation for Python codebases. It provides functionality for managing projects, updating docstrings, generating README files, and building a vectorstore for documents. The project uses the `langchain` library to set up a Q&A system with the Language Model (LLM) and generate docstrings and a README. It also includes a logger configuration for tracking and debugging issues.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Tests](#tests)
- [Information Used to Generate README](#information-used-to-generate-readme)

## Installation

To install the project, follow these steps:

1. Install the package using pip:

```bash
pip install gpt4docs
```

2. Add the OPENAI_API_KEY environment variable to your environment:

```bash
export OPENAI_API_KEY=your-api-key
```

## Usage

To use the project, make sure you have installed the required dependencies and set up the environment variables.

1. Run the application:

```bash
gpt4docs /path/to/your/project
```

For more help, run the base command or add the -h flag:

```bash
gpt4docs
```

or

```bash
gpt4docs -h
```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

### Setup

To set up the project for development, follow these steps:

1. Clone (or fork) the repository:

2. Install the dependencies:

```bash
make install
```

## Tests

To run tests, use the following command:

```bash
make test
```
