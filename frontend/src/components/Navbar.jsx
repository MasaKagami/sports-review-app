import React from "react";
import { Link } from "react-router-dom";
import AuthContext from "../context/AuthContext";

const Navbar = () => {
  const { user, logoutUser } = React.useContext(AuthContext);

  return (
    <nav>
      <div className="logo">
        <Link to="/">Logo</Link>
      </div>
      <div className="search-bar">
        <input type="text" placeholder="Search..." />
      </div>
      <div className="nav-links">
        <Link to="/games">Games</Link>
        <Link to="/members">Members</Link>
        <button>Create Entry</button>
      </div>
      <div className="user-profile">
        {user ? (
          <div className="dropdown">
            <img src={user.profilePicture} alt="Profile" />
            <div className="dropdown-content">
              <Link to="/profile">Profile</Link>
              <Link to="/settings">Settings</Link>
              <button onClick={logoutUser}>Logout</button>
            </div>
          </div>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
