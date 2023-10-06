const { spawn } = require('child_process');

// Replace 'path/to/your/python/script.py' with the actual path to your Python script
const pythonScriptPath = 'path/to/your/python/script.py';

// Replace 'OPENAI_API_KEY_VALUE' with the actual OpenAI API key
const openaiApiKey = 'OPENAI_API_KEY_VALUE';

// Example questions to pass to the Python script
const questions = ['What is the capital of France?', 'Who is the president of the United States?'];

// Spawn a new Python process
const pythonProcess = spawn('python', [pythonScriptPath, ...questions], {
  env: {
    OPENAI_API_KEY: openaiApiKey,
    ...process.env,  // Include the current environment variables
  },
});

// Capture the stdout of the Python script
pythonProcess.stdout.on('data', (data) => {
  console.log(`Python Script Output: ${data}`);
});

// Handle errors
pythonProcess.stderr.on('data', (data) => {
  console.error(`Error from Python Script: ${data}`);
});

// Handle the Python script's exit
pythonProcess.on('close', (code) => {
  console.log(`Python Script exited with code ${code}`);
});
