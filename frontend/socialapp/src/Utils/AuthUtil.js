import { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import VerifyToken from "./VerifyToken";

const AuthContext = createContext();
export default AuthContext;

const BASEURL = "http://127.0.0.1:8000/api"

export const AuthProvider = ({ children }) => {

    const [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);

    const [user, setUser] = useState(() => localStorage.getItem('authTokens') ? VerifyToken(localStorage.getItem('authTokens')) : null);

    const [loading, setLoading] = useState(true);

    const navigate = useNavigate();

    const loginUser = async (username, password) => {
        const resp = await fetch(`${BASEURL}/token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await resp.json(); // returns {'access': '<ACCESS_TOKEN>', 'refresh': '<REFRESH_TOKEN>'}
        if (resp.status === 200) {
            localStorage.setItem('authTokens', JSON.stringify(data));
            setAuthTokens(data);
            setUser(VerifyToken(data.access));
            navigate('/');
        }
    }

    const logoutUser = async (username, password) => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
        navigate('/login');
    }

    const registerUser = async (email, username, password, password2) => {
        const resp = await fetch(`${BASEURL}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, username, password, password2 })
        });
        if(resp.status === 201){
            loginUser(username, password);
        } else{
            console.log(resp.status);
        }
    }
    
    useEffect(() => {
        if (authTokens) {
            setUser(VerifyToken(authTokens.access))
        }
        setLoading(false);
    }, [authTokens, loading]);

    const contextData = {
        BASEURL,
        user,
        setUser,
        authTokens,
        setAuthTokens,
        loginUser,
        logoutUser,
        registerUser
    };

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    );
}