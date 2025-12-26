# Prompt Library Extension for Gemini CLI

A comprehensive collection of high-quality, pre-crafted prompts for common software engineering tasks, accessible via simple slash commands in the Gemini CLI.

## 📦 Installation

Install the extension using the Gemini CLI:

```bash
gemini extensions install yourusername/prompt-library-extension
```

Or install from a local directory:

```bash
git clone https://github.com/yourusername/prompt-library-extension.git
cd prompt-library-extension
gemini extensions link .
```

## 🚀 Quick Start

After installation, restart Gemini CLI and start using prompts:

```bash
# Review code for security issues
/code-review:security "your code here"

# Generate a README file
/docs:write-readme "describe your project"

# Create unit tests
/testing:generate-unit-tests "your function here"

# Explain a complex concept
/learning:explain-concept "recursion"

# Debug an error
/debugging:debug-error "paste your error here"
```

## 📋 Available Prompts

### 🔍 Code Review & Analysis
- `/code-review:security` - Deep security analysis
- `/code-review:performance` - Performance optimization
- `/code-review:best-practices` - Best practices review
- `/code-review:refactor` - Refactoring suggestions

### 📝 Documentation
- `/docs:write-readme` - Generate comprehensive README
- `/docs:write-api-docs` - Create API documentation
- `/docs:write-changelog` - Generate changelog
- `/docs:write-contributing` - Create contribution guidelines

### 🧪 Testing
- `/testing:generate-unit-tests` - Create unit tests
- `/testing:generate-e2e-tests` - Create end-to-end tests
- `/testing:edge-cases` - Identify edge cases
- `/testing:coverage-analysis` - Analyze test coverage

### 🐛 Debugging
- `/debugging:debug-error` - Diagnose and fix errors
- `/debugging:trace-issue` - Root cause analysis
- `/debugging:performance-profile` - Performance profiling

### 🏗️ Architecture & Design
- `/architecture:design-api` - Design RESTful APIs
- `/architecture:design-database` - Design database schemas
- `/architecture:system-design` - System architecture
- `/architecture:design-patterns` - Suggest design patterns

### 📚 Learning & Explanation
- `/learning:explain-concept` - Explain technical concepts
- `/learning:eli5` - Explain like I'm 5
- `/learning:compare-tech` - Compare technologies
- `/learning:roadmap` - Create learning paths

### ✍️ Writing & Communication
- `/writing:technical-blog` - Write technical posts
- `/writing:email` - Draft professional emails
- `/writing:presentation` - Create presentation outlines

### 🎨 Prompt Engineering
- `/prompts:improve` - Improve existing prompts
- `/prompts:create-template` - Create prompt templates
- `/prompts:best-practices` - Learn prompt tips

## 🛠️ Customization

### Adding Your Own Prompts
1. Create a new `.toml` file in the appropriate `commands/` subdirectory:
   ```bash
   mkdir -p commands/mycategory
   touch commands/mycategory/myprompt.toml
   ```
2. Write your prompt:
   ```toml
prompt = """
# My Custom Prompt

Your prompt content here with {{args}} for user input.
"""
   ```
3. Restart Gemini CLI to load the new prompt.

## 📚 Prompt Engineering Tips

1. **Be Specific**: Instead of "Review this code", use "Perform a security analysis focusing on input validation".
2. **Provide Structure**: Use clear sections, numbering, and formatting.
3. **Include Context**: Specify the language, framework, use case, and constraints.
4. **Request Examples**: Ask for code examples, not just explanations.
5. **Define Output Format**: Specify exactly how you want the response structured.
6. **Use Variables**: Make prompts reusable with `{{args}}` placeholders.
