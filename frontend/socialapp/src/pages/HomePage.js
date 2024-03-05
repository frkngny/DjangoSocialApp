import React, { useContext, useEffect, useState } from 'react'
import useAxios from "../Utils/useAxios";
import AuthContext from '../Utils/AuthUtil';

function HomePage() {
    const { user, logoutUser } = useContext(AuthContext);

    const [userStatus, setUserStatus] = useState("");

    const axios = useAxios();
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                const resp = await axios.get('http://localhost:8000/api/user-activity?user_id=' + user.user_id);
                setUserStatus(resp.data.status);
            } catch (error) {
                if (!user){
                    logoutUser();
                    return;
                }
                if (error.response.status !== 404)
                    logoutUser();
            }
        }
        fetchData();
    }, []);
    

    return (
        <div className="page-container">
            Hello
            Your status is {userStatus}
        </div>
    )
}

export default HomePage