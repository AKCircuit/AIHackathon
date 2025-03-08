import { useState } from "react"
import reactLogo from "./assets/react.svg"
import viteLogo from "/vite.svg"
import "./App.css"

const student = "student"
const supervisor = "supervisor"
const modules =  [
  "mechanics", "mech_vib", "thermo", "structures",
  "materials", "physical_principles_electronics",
  "analysis_of_circuits", "ac_power", "electromag",
  "digital", "maths", "computing"
]
const module_paper_questions = { // list of numbers a where a[i] is the number of questions in the i-th examples paper of a given module
  "mechanics": [3,2,5,6], 
  "mech_vib": [1], 
  "thermo": [9,9,5], 
  "structures": [,2,5,4,3],
  "materials": [12,4,4,6], 
  "physical_principles_electronics": [1,1,6,5,6],
  "analysis_of_circuits": [5],
  "ac_power": [13],
  "electromag": [12],
  "digital": [11],
  "maths": [6],
  "computing": [6],
  "*":[]
}
// function Hints({module}) {
//   console.log(module)
//   return (
//     <>
//       <p>hints</p>
//       <p>{modules[module]}</p>
//       {/* render papers/question dropdowns */}
//     </>
//   )

  

// }

function Question({moduleName, paperIndex}) { // TODO replace me with thing that gets hint data from server
  return (
    <li key={i} className="question-item">
      <a href={`/${moduleName}/paper${paperIndex + 1}/question${i + 1}`} className="question-link">
        Question {i + 1}
      </a>
    </li>
  )
}

const Hints = ({moduleId}) => {
  const [expandedPaper, setExpandedPaper] = useState(null);

  // Check if the specified moduleId exists in the data
  if (!moduleId || !module_paper_questions[moduleId]) {
    return <div className="module-menu-error">Module not found</div>;
  }

  const papers = module_paper_questions[moduleId];
  
  const handlePaperClick = (paperIndex) => {
    setExpandedPaper(expandedPaper === paperIndex ? null : paperIndex);
  };
  if (moduleId != "*") {
    return (
      <nav className="module-menu">
        <div className="module-header">
          {moduleId.replace('_', ' ')}
        </div>
        
        <ul className="paper-list">
          {papers.map((questionCount, paperIndex) => (
            <li key={paperIndex} className="paper-item">
              <button 
                className={`paper-button ${expandedPaper === paperIndex ? 'expanded' : ''}`}
                onClick={() => handlePaperClick(paperIndex)}
              >
                Paper {paperIndex + 1} ({questionCount} questions)
              </button>
              
              {expandedPaper === paperIndex && (
                <ul className="question-list">
                  {Array.from({ length: questionCount }, (_, i) => (
                    <li key={i} className="question-item">
                      <a href={`/${moduleId}/paper${paperIndex + 1}/question${i + 1}`} className="question-link">
                        Question {i + 1}
                      </a>
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      </nav>
    );
  }
  else {
    return (
      <nav className="module-menu">
        <ul className="module-list">
          {Object.entries(module_paper_questions).filter(([moduleName,_])=>(moduleName!="*")).map(([moduleName, papers]) => (
            <li key={moduleName} className="module-item">
              <button 
                className={`module-button ${expandedModule === moduleName ? 'expanded' : ''}`}
                onClick={() => handleModuleClick(moduleName)}
              >
                {moduleName.replace('_', ' ')}
              </button>
              
              {expandedModule === moduleName && (
                <ul className="paper-list">
                  {papers.map((questionCount, paperIndex) => (
                    <li key={paperIndex} className="paper-item">
                      <button 
                        className={`paper-button ${expandedPaper === paperIndex ? 'expanded' : ''}`}
                        onClick={() => handlePaperClick(paperIndex)}
                      >
                        Paper {paperIndex + 1} ({questionCount} questions)
                      </button>
                      
                      {expandedPaper === paperIndex && (
                        <ul className="question-list">
                          {Array.from({ length: questionCount }, (_, i) => (
                            <Question moduleName={moduleName} paperIndex={paperIndex} />
                            
                          ))}
                        </ul>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      </nav>
    );
  }
};

function CrsidInput() {
  return (
    <>
      <p>crsid input</p>
    </>
  )
}

function ModuleSearchDropdown({results = [], setModule}) {
  // Render list of seach results

  function handleSelectResult(result) {
    setModule(result.id)
  }
  console.log("isarray " + Array.isArray(results))
  console.log("l>0" + results.length > 0  )
  console.log(results)
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
                {result.description && (
                  <div className="result-description">{result.description}</div>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <div className="no-results">No results found</div>
        )}
      </div>
    </>
  )
}

function ModuleSearch({setModule}) {
  let [searchActive, setSearchActive] = useState(false)
  let [results, setResults] = useState([])
  return (
    <>
      <p>module search</p>
      <input type="text" placeholder="search modules..." onChange={(event) => {
        // simple search for now
        const searchTerm = event.target.value.toLowerCase();
        const filtered = modules.filter(m => m.replace(/_/g, " ").includes(searchTerm));
        let newResults = []
        for (let element of filtered) {
          newResults.push({
            id: modules.indexOf(element),
            title: ((m) => m.replace(/_/g, " "))(element)
          })
        }
        // show top 3 at most
        newResults = newResults.slice(0,3);
        setResults(newResults);
        searchTerm.length ? setSearchActive(true) : setSearchActive(false)
      }} onKeyUp={(event) => {
        if (event.key !== "Enter") return;
        setModule(results[0].id)
        setSearchActive(false)
        event.target.value = ""
      }}></input>
      {searchActive && <ModuleSearchDropdown results={results} setModule={setModule} />}
    </>
  )
}

function StudentDashboard({module, setModule}) {
  return (
    <>
      <p>student dashboard</p>
      <ModuleSearch setModule={setModule} />
      <Hints moduleId={modules[module]} />
    </>
  )
}

function SupervisorDashboard() {
  return (
    <>
      <p>supervisor dashboard</p>
      <CrsidInput />
      <Hints  moduleId={"*"}/>
    </>
  )
}

function Dashboard({userType, module, setModule}) {
  return (
    <>
      {(userType === student) && <StudentDashboard module={module} setModule={setModule} />}
      {(userType === supervisor) && <SupervisorDashboard />}
    </>
  )
}

function LoginFailed() {
  return (
    <>
      <p>Login failed.</p>
    </>
  )
}

function Login({setLoggedIn, setUserType}) {

  let loginFailed, setLoginFailed = useState()
  
  return (
    <>
      <p>Login</p>
      <form onSubmit={(event) => {
            // Real behaviour:
            // send username and password to server
            // on success, set usertype and loggedin
            // otherwise set loginFailed to true 

            // Dummy
            event.preventDefault()
            setLoggedIn(true)
            setUserType(student)
      }}>  
      <input type="username" placeholder="username"></input>
        <input type="password" placeholder="password"></input>
        <button type="submit">log in</button>
      </form>
      {loginFailed && <LoginFailed />}
    </>
  )
}

function App() {
 
  let [loggedIn, setLoggedIn] = useState(false)
  let [userType, setUserType] = useState(student)
  let [module, setModule] = useState(0)
  return (
    <>
      <div>
        {!loggedIn && <Login setLoggedIn={setLoggedIn} setUserType={setUserType} />}
      </div>
      <div>
        {loggedIn && <Dashboard userType={userType} module={module} setModule={setModule} />}
      </div>
    </>
  )
}

export default App
