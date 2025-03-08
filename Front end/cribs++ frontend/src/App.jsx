import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function StudentDashboard() {
  return (
    <>
      <ModuleSearch />
      <Hints />
    </>
  )
}

function SupervisorDashboard() {
  return (
    <>
      <StudentInput />
      <Hints />
    </>
  )
}

function Dashboard() {
  return (
    <>
      {(userType == student) && <StudentDashboard />}
      {(userType == supervisor) && <SupervisorDashboard />}
    </>
  )
}

function Login() {
  return (
    <>
      <form>  
      <input type="username" name="student-username" id="student-username" placeholder="username"></input>
        <input type="password" name="student-password" id="student-password" placeholder="password"></input>
        <button type="submit">log in</button>
      </form>
    </>
  )
}

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        {!loggedIn && <Login />}
      </div>
      <div>
        {loggedIn && <Dashboard />}
      </div>
    </>
  )
}

export default App
