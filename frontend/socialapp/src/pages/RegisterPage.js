import React, { useContext, useState } from 'react'
import AuthContext from '../Utils/AuthUtil';
import { Link } from 'react-router-dom';

function RegisterPage() {
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");

    const { registerUser } = useContext(AuthContext);

    const handleFormSubmit = (e) => {
        e.preventDefault();
        registerUser(email, username, password, password2);
    }

    return (
        <div className="page-container">
            <form onSubmit={handleFormSubmit}>
                <div>
                    <label htmlFor='txtUsername'>Username</label>
                    <input type='text' id='txtUsername' name='username' onChange={e => setUsername(e.target.value)}/>
                </div>
                <div>
                    <label htmlFor='txtEmail'>Email Address</label>
                    <input type='email' id='txtEmail' name='email' onChange={e => setEmail(e.target.value)}/>
                </div>
                <div>
                    <label htmlFor='txtPassword'>Password</label>
                    <input type='password' id='txtPassword' name="password" onChange={e => setPassword(e.target.value)}/>
                </div>
                <div>
                    <label htmlFor='txtPassword2'>Confirm Password</label>
                    <input type='password' id='txtPassword2' name="password2" onChange={e => setPassword2(e.target.value)}/>
                </div>
                <button type='submit'>Register</button>
            </form>
            <Link to="/login">Already have an account?</Link>
        </div>
    )
}

export default RegisterPage