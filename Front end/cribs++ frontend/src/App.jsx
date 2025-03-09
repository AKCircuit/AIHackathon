import { useState, useContext, createContext, useEffect } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

// TODO add in code to request from server

// backend API url
const url = "http://localhost:5000/process"

// Create contexts
const UserContext = createContext(null);
const ModuleContext = createContext(null);

// User types
const student = "student";
const supervisor = "supervisor";

// Module data
const modules = [
  "mechanics", "mech_vib", "thermo", "structures",
  "materials", "physical_principles_electronics",
  "analysis_of_circuits", "ac_power", "electromag",
  "digital", "maths", "computing"
];

const module_paper_questions = {
  "mechanics": [3, 2, 5, 6],
  "mech_vib": [1],
  "thermo": [9, 9, 5],
  "structures": [1, 2, 5, 4, 3],
  "materials": [12, 4, 4, 6],
  "physical_principles_electronics": [1, 1, 6, 5, 6],
  "analysis_of_circuits": [5],
  "ac_power": [13],
  "electromag": [12],
  "digital": [11],
  "maths": [6],
  "computing": [6],
  "*": []
};

// Custom context hooks
function useUser() {
  return useContext(UserContext);
}

function useModule() {
  return useContext(ModuleContext);
}

function Hint({ moduleName, paperIndex, questionId, hintId, supervisee = null }) {
  const { user } = useUser();
  const [isRevealed, setIsRevealed] = useState(false);
  const [hintText, setHintText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Check if hint was previously revealed
  async function fetchIsRevealed(crsid, moduleName, paperIndex, questionId, hintId) {
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Accept":"application/json", 
          "Content-Type":"application/json"
        },
        body: JSON.stringify({"user_seen_hint":{
          "module": moduleName,
          "paper_no": paperIndex + 1,
          "question_no": questionId + 1,
          "hint_no": hintId,
          "user_name": crsid
        }})
      });
      
      if (!response.ok) {
        throw new Error("fetchIsRevealed failed :(");
      }
      
      const json = await response.json();
      const revealed = json["seen_hint"];
      setIsRevealed(revealed);
      
      // If hint was previously revealed, fetch the hint content
      if (revealed) {
        await fetchHintContent(crsid, moduleName, paperIndex, questionId, hintId);
      }
    } catch (error) {
      console.error(error.message);
      setError("this hint does not exist!");
    }
  }

  // Fetch the actual hint content
  async function fetchHintContent(crsid, moduleName, paperIndex, questionId, hintId) {
    setIsLoading(true);
    try {
      const request = {
        method: "POST",
        headers: {
          "Accept":"application/json", 
          "Content-Type":"application/json"
        },
        body: JSON.stringify({"get_hint": {
          "module": moduleName,
          "paper_no": paperIndex + 1,
          "question_no": questionId + 1,
          "hint_no": hintId,
          "user_name": crsid
        }})
      };
      
      const response = await fetch(url, request);
      
      if (!response.ok) {
        throw new Error(`Getting hint for ${moduleName} paper ${paperIndex + 1} question ${questionId + 1} hint ${hintId} failed.`);
      }
      
      const json = await response.json();
      setHintText(json["hint"]);
    } catch (error) {
      console.error(error.message);
      setError("Failed to load hint content");
      setHintText("Hint failed to load :(");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    // Check if hint was previously revealed on component mount
    const effectiveCrsid = supervisee !== null ? supervisee : user;
    fetchIsRevealed(effectiveCrsid, moduleName, paperIndex, questionId, hintId);
  }, [user, supervisee, moduleName, paperIndex, questionId, hintId]);

  const revealHint = async () => {
    if (supervisee !== null) {
      return; // Supervisors can't reveal hints for students
    }

    // Can only be set to true, never back to false
    setIsRevealed(true);
    setIsLoading(true);
    
    try {
      // Record that hint has been viewed
      const revealResponse = await fetch(url, {
        method: "POST",
        headers: {
          "Accept":"application/json", 
          "Content-Type":"application/json"
        },
        body: JSON.stringify({
          "record_hint_viewed": {
            "module": moduleName,
            "paper_no": paperIndex + 1,
            "question_no": questionId + 1,
            "hint_no": hintId,
            "user_name": user
          }
        })
      });
      
      if (!revealResponse.ok) {
        throw new Error("Failed to record hint view");
      }
      
      // Fetch the hint content
      await fetchHintContent(user, moduleName, paperIndex, questionId, hintId);
    } catch (error) {
      console.error(error.message);
      setError("Failed to reveal hint");
    }
  };

  return (
    <li className="hint-item">
      <div className="hint-container">
        <label className="hint-checkbox-label">
          <input
            type="checkbox"
            checked={isRevealed}
            onChange={revealHint}
            disabled={isRevealed || isLoading} // Disable when checked or loading
            className="hint-checkbox"
          />
          <span className="hint-label">{supervisee ? supervisee + " " : "" }{isRevealed?"":" has not "}reveal{supervisee?"ed":""} hint {hintId}</span>
        </label>

        {isLoading && <div className="loading">Loading hint...</div>}
        {error && <div className="error">{error}</div>}
        
        {isRevealed && !isLoading && (
          <div className="hint-content">
            {hintText || `Content for hint ${hintId} would appear here`}
          </div>
        )}
      </div>
    </li>
  );
}

function HintFailed() {
  return (
    <>
      <p>hint failed to load :&#40;</p>
    </>
  );
}

function Question({ moduleName, paperIndex, questionIndex, supervisee = null }) {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const user = useContext(UserContext);
  
  // Hardcoded hint count since backend doesn't support metadata fetching yet
  const hintCount = 2;
  const availableHints = Array.from({ length: hintCount }, (_, i) => i + 1);

  const toggleOpen = (event) => {
    event.preventDefault();
    setIsOpen(!isOpen);
  };

  return (
    <li className="question-item">
      <div className="question-container">
        <button
          onClick={toggleOpen}
          className={`question-button ${isOpen ? 'open' : ''}`}
        >
          Question {questionIndex + 1}
        </button>

        {isOpen && (
          <div className="hints-container">
            {error && <HintFailed />}
            <ul className="hints-list">
              {availableHints.map(hintId => (
                <Hint
                  key={hintId}
                  moduleName={moduleName}
                  paperIndex={paperIndex}
                  questionId={questionIndex}
                  hintId={hintId}
                  supervisee={supervisee}
                />
              ))}
            </ul>
          </div>
        )}
      </div>
    </li>
  );
}
// Extracted component for question lists
const QuestionList = ({ moduleName, paperIndex, questionCount, supervisee }) => {
  return (
    <ul className="question-list">
      {Array.from({ length: questionCount }, (_, i) => (
        <Question
          key={i}
          moduleName={moduleName}
          paperIndex={paperIndex}
          questionIndex={i}
          supervisee={supervisee}
        />
      ))}
    </ul>
  );
};

// Extracted component for paper items
const PaperItem = ({ paperIndex, questionCount, expandedPaper, handlePaperClick, moduleName, supervisee }) => {
  return (
    <li key={paperIndex} className="paper-item">
      <button
        className={`paper-button ${expandedPaper === paperIndex ? 'expanded' : ''}`}
        onClick={() => handlePaperClick(paperIndex)}
      >
        paper {paperIndex + 1} ({questionCount} question{questionCount > 1 ? "s" : ""})
      </button>

      {expandedPaper === paperIndex && (
        <QuestionList
          moduleName={moduleName}
          paperIndex={paperIndex}
          questionCount={questionCount}
          supervisee={supervisee}
        />
      )}
    </li>
  );
};

// Main component
const Hints = ({ supervisee = null }) => {
  const { selectedModuleId } = useModule();
  const [expandedPaper, setExpandedPaper] = useState(null);
  const [expandedModule, setExpandedModule] = useState(null);

  // Check if the specified moduleId exists in the data
  if (!selectedModuleId || !module_paper_questions[selectedModuleId]) {
    return <div className="module-menu-error"></div>;
  }

  const papers = module_paper_questions[selectedModuleId];

  const handlePaperClick = (paperIndex) => {
    setExpandedPaper(expandedPaper === paperIndex ? null : paperIndex);
  };

  const handleModuleClick = (moduleName) => {
    setExpandedModule(expandedModule === moduleName ? null : moduleName);
    setExpandedPaper(null); // Reset expanded paper when changing modules
  };

  // Render papers for a single module
  if (selectedModuleId !== "*") {
    return (
      <nav className="module-menu">
        <div className="module-header">
          <h3>{selectedModuleId.replaceAll('_', ' ')}</h3>
        </div>

        <ul className="paper-list">
          {papers.map((questionCount, paperIndex) => (
            <PaperItem
              key={paperIndex}
              paperIndex={paperIndex}
              questionCount={questionCount}
              expandedPaper={expandedPaper}
              handlePaperClick={handlePaperClick}
              moduleName={selectedModuleId}
              supervisee={supervisee}
            />
          ))}
        </ul>
      </nav>
    );
  }

  // Render all modules
  return (
    <nav className="module-menu">
      <ul className="module-list">
        {Object.entries(module_paper_questions)
          .filter(([moduleName, _]) => (moduleName !== "*"))
          .map(([moduleName, papers]) => (
            <li key={moduleName} className="module-item">
              <button
                className={`module-button ${expandedModule === moduleName ? 'expanded' : ''}`}
                onClick={() => handleModuleClick(moduleName)}
              >
                {moduleName.replaceAll('_', ' ')}
              </button>

              {expandedModule === moduleName && (
                <ul className="paper-list">
                  {papers.map((questionCount, paperIndex) => (
                    <PaperItem
                      key={paperIndex}
                      paperIndex={paperIndex}
                      questionCount={questionCount}
                      expandedPaper={expandedPaper}
                      handlePaperClick={handlePaperClick}
                      moduleName={moduleName}
                      supervisee={supervisee}
                    />
                  ))}
                </ul>
              )}
            </li>
          ))}
      </ul>
    </nav>
  );
};


function CrsidInput({ setSupervisee }) {
  return (
    <>
      <input
        type="text"
        placeholder="enter student's crsid"
        onKeyUp={(event) => {
          if (event.key !== "Enter") return;
          setSupervisee(event.target.value)
          event.target.value = "";
        }}
      />
    </>
  );
}

function ModuleSearch() {
  const [searchActive, setSearchActive] = useState(false);
  const [results, setResults] = useState([]);
  const { setSelectedModule } = useModule(); // Move hook call here

  return (
    <>
      <input
        type="text"
        placeholder="search modules..."
        onChange={(event) => {
          // simple search for now
          const searchTerm = event.target.value.toLowerCase();
          const filtered = modules.filter(m => m.replace(/_/g, " ").includes(searchTerm));
          let newResults = [];

          for (let element of filtered) {
            newResults.push({
              id: element, // Use the actual module name as ID
              title: element.replace(/_/g, " ")
            });
          }

          // show top 3 at most
          newResults = newResults.slice(0, 3);
          setResults(newResults);
          searchTerm.length ? setSearchActive(true) : setSearchActive(false);
        }}
        onKeyUp={(event) => {
          if (event.key !== "Enter" || results.length === 0) return;
          setSelectedModule(results[0].id); // Use it directly here
          setSearchActive(false);
          event.target.value = "";
        }}
      />
      {searchActive && <ModuleSearchDropdown
        results={results}
        setSelectedModule={setSelectedModule} // Pass as prop
      />}
    </>
  );
}

function ModuleSearchDropdown({ results = [], setSelectedModule }) {
  // Remove the useModule hook from here

  function handleSelectResult(result) {
    setSelectedModule(result.id);
  }

  return (
    <>
      <div>
        {Array.isArray(results) && results.length > 0 ? (
          <ul className="results-list">
            {results.map((result) => (
              <li
                key={result.id}
                className="result-item"
                onClick={() => handleSelectResult(result)}
              >
                <div className="result-title">{result.title}</div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="no-results">No results found</div>
        )}
      </div>
    </>
  );
}

function StudentDashboard() {
  return (
    <>
      <h2>student dashboard</h2>
      <ModuleSearch />
      <Hints />
    </>
  );
}

function MonitoredStudent({supervisee = null}) {
  return (
    <>
    {supervisee && <p>monitoring {supervisee}</p>}
    </>
  )
}

function SupervisorDashboard() {
  const [supervisee, setSupervisee] = useState(""); // supervisees are uniquely defined by their CRSIDs
  const { setSelectedModule } = useModule();

  return (
    <>
      <h2>supervisor dashboard</h2>
      <CrsidInput setSupervisee={setSupervisee} />
      <MonitoredStudent supervisee={supervisee}/>
      <ModuleSearch />
      <Hints supervisee={supervisee} />
    </>
  );
}

function Dashboard() {
  const { userType } = useUser();

  return (
    <>
      {userType === student && <StudentDashboard />}
      {userType === supervisor && <SupervisorDashboard />}
    </>
  );
}

function LoginFailed() {
  return (
    <>
      <p>Login failed.</p>
    </>
  );
}

function Login({ setLoggedIn }) {
  const { setUser, setUserType } = useUser();
  const [loginFailed, setLoginFailed] = useState(false);

  return (
    <>
      <form onSubmit={async (event) => {
        // Real behaviour:
        // send username and password to server
        // on success, set usertype and loggedin
        // otherwise set loginFailed to true 
        event.preventDefault()
        try {
          const response = await fetch(url, { // Login works - use TestUser1:defg
            method: "POST",
            headers: {
              "Accept":"application/json", 
              "Content-Type":"application/json"
            },
            body: JSON.stringify({"authenticate": {
              "user_name": event.target.elements.username.value, 
              "pw": event.target.elements.password.value}})
          })
          if (!response.ok) {
            throw new Error(`Response status: ${response.status}`)
          }
          const json = await response.json()
          setUser(event.target.elements.username.value)
          setUserType(json["role"])
          setLoggedIn(true)
          setLoginFailed(false)
        } catch (error) {
          console.error(error.message);
          setLoginFailed(true)
        }

        // Dummy
        // event.preventDefault();
        // setLoggedIn(true);
        // setUserType(supervisor);
        // setUser("ab123");
      }}>
        <h2> log in </h2>
        <input type="username" name="username" placeholder="username"></input> <br />
        <input type="password"  name="password" placeholder="password"></input><br />
        <button type="submit">log in</button>
      </form>
      {loginFailed && <LoginFailed />}
    </>
  );
}

function SignupFailed() {
  return (
    <>
      <p>Sign up failed.</p>
    </>
  );
}

function Signup({ setLoggedIn }) {
  const { setUser, setUserType } = useUser();
  const [signupFailed, setSignupFailed] = useState(false)
  return (
    <>
      <form onSubmit={async (event) => {
        // Real behaviour:
        // send username and password to server to register
        // on success, login the user
        // otherwise set signupFailed to true 
        event.preventDefault()
        try {
          const response = await fetch(url, {
            method: "POST",
            body: JSON.stringify({"register_user": {
              "user_name": event.target.elements.username.value, 
              "pw": event.target.elements.password.value,
              "role": event.target.elements.supervisorMode.value ? supervisor : student}})
          })
          if (!response.ok) {
            throw new Error(`Response status: ${response.status}`)
          }
          const json = await response.json()
          setUser(event.target.elements.username.value)
          setUserType(json["role"])
          setLoggedIn(true)
          setSignupFailed(false)
        } catch (error) {
          console.error(error.message);
          setSignupFailed(true)
        }
        // Dummy
        // event.preventDefault();
        // setLoggedIn(true);
        // setUserType(student);
        // setUser("ab123");
      }}>
        <h2>sign up</h2>
        <input type="username" name="username" placeholder="username"></input> <br />
        <input type="password" name="password" placeholder="password"></input><br />
        <input id="supervisor-mode" name="supervisorMode" type="checkbox"></input>
        <label for="supervisor-mode"> supervisor mode &gt;:&#41;</label>
        <p></p><br />
        <button type="submit">sign up</button>
      </form>
      {signupFailed && <SignupFailed />}
    </>
  );
}

function App() {
  // App-level state
  const [loggedIn, setLoggedIn] = useState(false);

  // User context state
  const [user, setUser] = useState("");
  const [userType, setUserType] = useState(student);

  // Module context state
  const [selectedModule, setSelectedModule] = useState(-1);
  const [selectedModuleId, setSelectedModuleId] = useState("");

  // Update selectedModuleId whenever selectedModule changes
  useEffect(() => {
    if (typeof selectedModule === 'number') {
      setSelectedModuleId(modules[selectedModule]);
    } else {
      // Handle case where selectedModule is already a string (module name)
      setSelectedModuleId(selectedModule);
    }
  }, [selectedModule]);

  // Context value objects
  const userContextValue = {
    user,
    setUser,
    userType,
    setUserType
  };

  const moduleContextValue = {
    selectedModule,
    setSelectedModule,
    selectedModuleId,
    setSelectedModuleId
  };

  return (
    <UserContext.Provider value={userContextValue}>
      <ModuleContext.Provider value={moduleContextValue}>
        <div>
          {!loggedIn && <>

            <h1>cribs++</h1>
            <Login setLoggedIn={setLoggedIn} /> <Signup />
          </>}
        </div>
        <div>
          {loggedIn && <Dashboard />}
        </div>
      </ModuleContext.Provider>
    </UserContext.Provider>
  );
}

export default App;