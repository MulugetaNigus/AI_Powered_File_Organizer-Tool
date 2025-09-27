# File Organizer Tool

This AI-powered tool helps organize files in a directory based on user instructions. It uses OpenRouter's API to intelligently categorize and move files.

## Features

- **Navigate to Folders**: Change the working directory to a specified folder.
- **List Directory Contents**: View files and folders in the current directory.
- **Create Folders**: Make new folders for organization.
- **Copy Files**: Move files to appropriate folders.
- **AI-Driven Organization**: Use natural language to specify how to organize files (e.g., by type, date, etc.).
- **Detailed Logging**: See step-by-step what the AI is doing, including thinking, tool calls, and results.

## Prerequisites

- Python 3.8 or higher
- An OpenRouter API key (get one from [openrouter.ai](https://openrouter.ai))

## Installation

1. **Clone or Download**: Place the `file_Organizer` folder in your desired location.

2. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   - Copy `.env.example` to `.env`.
   - Add your OpenRouter API key to `.env`:
     ```
     OPENROUTER_API_KEY=your_actual_api_key_here
     ```

## Usage

1. **Navigate to the Directory**: Open a terminal and go to the folder you want to organize. The tool will run in the current directory by default, but you can specify a different folder in your input.

2. **Run the Tool**:
   ```
   python watch_file.py
   ```

3. **Provide Instructions**: When prompted, enter how you want to organize the files. For example:
   - "Organize files in the current directory by file type."
   - "Navigate to 'downloads' folder and organize by date."
   - "Create folders for images, documents, and videos, then copy files accordingly."

4. **Monitor Progress**: The tool will log each AI thought, tool call, and action taken, so you can follow along.

## Example

```
$ python watch_file.py
How do you want organize your files and tell me which folders you want me to watch for file organizations?: Organize files in the current directory by type.

[Logging output shows AI planning, listing directory, creating folders, copying files...]

Final summary of organization.
```

## Notes

- The tool uses the current working directory as the starting point. If you want to organize a specific folder, mention it in your input prompt, and the AI will navigate there.
- Ensure your `.env` file is not committed to version control (it's already in `.gitignore`).
- The AI model is "x-ai/grok-4-fast:free" via OpenRouter. You can modify the model in the code if needed.
- Be cautious with file operations; the tool can move files, so review the logs.

## Troubleshooting

- If you get API errors, check your API key and internet connection.
- For permission issues, ensure Python has access to the directories.
- Virtual environment issues: The tool includes a `pyvenv.cfg` for the virtual env, but you may need to adjust paths if your Python installation differs.

## License

This project is open-source. Use at your own risk.
