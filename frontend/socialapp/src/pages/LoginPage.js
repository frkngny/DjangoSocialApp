import React, { useContext } from 'react'
import AuthContext from '../Utils/AuthUtil'
import { Link } from 'react-router-dom';

function LoginPage() {
    const { loginUser } = useContext(AuthContext);

    const handleFormSubmit = (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;
        username.length > 0  && loginUser(username, password);
    };

    return (
        <div className="page-container">
            <form onSubmit={handleFormSubmit}>
                <div>
                    <label htmlFor='txtUsername'>Username</label>
                    <input type='text' id='txtUsername' name='username'/>
                </div>
                <div>
                    <label htmlFor='txtPassword'>Password</label>
                    <input type='password' id='txtPassword' name="password"/>
                </div>
                <button type='submit'>Login</button>
            </form>
            <Link to="/register">Don't have an account?</Link>
        </div>
    )
}

export default LoginPage