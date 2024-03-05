import React from 'react'
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import HomePage from './pages/HomePage'
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';
import { AuthProvider } from './Utils/AuthUtil';
import Navbar from './components/Navbar';
import ProfilePage from './pages/ProfilePage';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Navbar/>
        <Routes>
          <Route exact path='/' element={<HomePage />}/>
          <Route path='/register' element={<RegisterPage/>}/>
          <Route path='/login' element={<LoginPage/>}/>
          <Route path='/profile/:username' element={<ProfilePage/>}/>
        </Routes>
      </AuthProvider>
    </Router>
  )
}

export default App;