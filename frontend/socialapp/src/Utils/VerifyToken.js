import { jwtDecode } from "jwt-decode";

const VerifyToken = (token) => {
    return jwtDecode(token);
}
export default VerifyToken;