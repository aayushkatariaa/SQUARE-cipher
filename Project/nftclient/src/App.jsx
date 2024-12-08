
import React, { useState } from "react";
import {
  BrowserRouter as Router,
  Link,
} from "react-router-dom";
import RoutesPage from "./routes";
const AuthApi = React.createContext();
const TokenApi = React.createContext();
import Cookies from "js-cookie";
function App() {
  const [auth, setAuth] = useState(false);
  const [token, setToken] = useState("");
  const readCookie = () => {
    let token = localStorage.getItem("access_token");
    if (token) {
      setAuth(true);
      setToken(token);
    }
  };
  React.useEffect(() => {
    readCookie();
  }, []);
  
  return (
    <>
      <AuthApi.Provider value={{ auth, setAuth }}>
        <TokenApi.Provider value={{ token, setToken }}>
          <Router>
            <div>
              <nav>
                <ul>
                  {!auth ? (
                    <li>
                      <Link to="/register">Regsiter</Link>
                    </li>
                  ) : (
                    <></>
                  )}
                  {!auth ? (
                    <li>
                      <Link to="/login">Login</Link>
                    </li>
                  ) : (
                    <></>
                  )}
                  <li>
                    <Link to="/">Home</Link>
                  </li>
                </ul>
              </nav>
              <RoutesPage />
            </div>
          </Router>
        </TokenApi.Provider>
      </AuthApi.Provider>
    </>
  );
}



export { AuthApi, TokenApi };
export default App;