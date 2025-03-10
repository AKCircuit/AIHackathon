# Cribs++
#### An AI-powered platform that analyses academic contents to provide real-time support for skill gaps

README
________
### Authors (in alphabetical order)
*  Usairam Abdullah
* Adam Kerbel
* Eric Li
* Jadon Mensah

### System Requirements for Server Host
#### Windows, Mac or Linux systems that supports:
* Python 3.9 or newer versions
* node.js or equivalent JavaScript runtime environment
##### Install these Python Packages before running server: 
* openai 
* pydantic 
* dotenv 
* pymupdf 
* flask 
* flask_cors
* base64
* sqlite3
* atexit

##### Install these Javascript frameworks and packages
* react
* npm
* katex
* react-latex-next

### Installation and program run
* Download the server program and unzip into a single directory, the root directory of program.
* Create a new file named .env in the root directory of the program. The Server host will have to provide their own OpenAI API Keys.
* The Template for .env is provided in the .env.example file in the root directory. Enter your API key in the first row, your User ID in the second row: DB_USER, and your Project ID in third row: DB_PASSWORD.
* Set the Python run directory as the root directory, and run server.py. This starts back-end server.
* Open Command Prompt on your system and change the directory to Front end/cribs++ frontend
* Run the command: npm run dev. This runs the front-end server
* If the above does not work, reopen the command shell in admin mode and repeat the above two procedures.
* We found a common error to be related to the Windows PowerShell's execution policy, and our solution was temporarily bypassing the execution policy with the following command: PowerShell -ExecutionPolicy Bypass

### Client use
* Open a Web Browser and open the address indicated by the front-end server.
* Sign up a new account and choose whether you are a student or a supervisor, or log on an existing account
* Choose from the set of example papers provided in our existing database and hints are provided.

### Version History
* 1.0 Completed reading text pdfs from example papers on CamCribs as part of Database
* 2.0 Can now read handwritten pdfs and scanned documents and the Cribs are part of the Database.

### Please report any bugs to the group.


