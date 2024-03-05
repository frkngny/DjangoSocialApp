import axios from "axios"
import dayjs from "dayjs"
import { useContext } from "react"
import AuthContext from "./AuthUtil"
import VerifyToken from "./VerifyToken"

const BASEURL = "http://127.0.0.1:8000/api"

const useAxios = () => {
    const { authTokens, setUser, setAuthTokens } = useContext(AuthContext);
    const axiosInstance = axios.create({
        BASEURL,
        headers: { Authorization: `Bearer ${authTokens?.access}` }
    });

    axiosInstance.interceptors.request.use(async request => {
        const user = VerifyToken(authTokens.access);
        const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;
        if(!isExpired) return request;

        const resp = await axios.post(`${BASEURL}/token-refresh`, {
            refresh: authTokens.refresh, 
            headers: { Authorization: `Bearer ${authTokens.access}` }
        });

        localStorage.setItem('authTokens', JSON.stringify(resp.data));
        setAuthTokens(resp.data);
        setUser(VerifyToken(resp.data.access));
        request.headers.Authorization = `Bearer ${authTokens.access}`;
        return request;
    });

    return axiosInstance;
}

export default useAxios;