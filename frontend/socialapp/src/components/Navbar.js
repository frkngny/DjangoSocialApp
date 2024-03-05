import React, { useContext, useEffect, useState } from 'react'
import AuthContext from '../Utils/AuthUtil'
import Avatar from "@mui/material/Avatar"
import useAxios from '../Utils/useAxios';

function Navbar() {
    const { user, logoutUser, BASEURL } = useContext(AuthContext);
    const token = localStorage.getItem('authTokens');
    const [userImage, setUserImage] = useState("");
    const axios = useAxios();

    useEffect(() => {
        if (user)
            axios.get(`${BASEURL}/profile/` + user.user_id).then((resp) => {
                setUserImage(resp.data.image);
            })
    }, []);

    return (
        <div className='custom-nav'>
            <nav className="navbar navbar-expand-lg navbar-dark sticky-top bg-dark">
                <div className="container-fluid">
                    <a className="navbar-brand" href="#">
                        <img style={{ width: "120px", padding: "6px" }} src="" alt="" />
                    </a>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarNav">
                        <ul className="navbar-nav ">
                            <li className="nav-item">
                                <a className="nav-link active" aria-current="page" href="/">Home</a>
                            </li>
                            {
                                token === null ?
                                    <>
                                        <li className="nav-item">
                                            <a className="nav-link active" href="/login">Login</a>
                                        </li>
                                        <li className="nav-item">
                                            <a className="nav-link active" href="/register">Register</a>
                                        </li>
                                    </>
                                    :
                                    <>
                                        {/* <li className="nav-item">
                                            <a className="nav-link" href="/dashboard">Dashboard</a>
                                        </li>
                                        <li className="nav-item">
                                            <a className="nav-link" href="/inbox">Inbox</a>
                                        </li> */}
                                        <li className="nav-item">
                                            <a className="nav-link" onClick={logoutUser} style={{ cursor: "pointer" }}>Logout</a>
                                        </li>
                                    </>
                            }
                        </ul>
                        
                    </div>
                    { token !== null && 
                        <div className='d-flex'>
                            <a href="/profile">
                                <Avatar alt="" src={userImage} />
                            </a>
                        </div>
                    }
                </div>
            </nav>
        </div>
    )
}

export default Navbar