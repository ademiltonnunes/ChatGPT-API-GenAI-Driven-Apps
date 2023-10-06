import { exec } from 'child_process';
import path from 'path';

export default async function (req, res) {
  const question = req.body.question || '';
  if (question.trim().length === 0) {
    res.status(400).json({
      error: {
        message: "Please enter a valid question",
      },
    });
    return;
  }

  try {
    const pythonScriptPath = 'python_script.py';
    const scriptPath = path.join(__dirname, 'python_script.py');
    const scriptArguments = [question];
    const command = `python ${pythonScriptPath} ${scriptArguments.join(' ')}`;

    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing Python script: ${error}`);
        return res.status(500).json({
          error: {
            message: 'An error occurred during script execution.',
          },
        });
      }

      console.log('Python script output:');
      console.log(stdout);
      res.status(200).json({ result: stdout });
    });
  } catch (error) {
    console.error(`Error: ${error.message}`);
    res.status(500).json({
      error: {
        message: 'An error occurred during your request.',
      },
    });
  }
}