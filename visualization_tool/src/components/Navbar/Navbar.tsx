import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';

import './Navbar.css';
import logo from '/logo.png';

const Navbar = () => {
  return (
    <>
      <header>
        <img src={logo} className="logo" alt="GCP Scanner logo" />
        <p>Scanner</p>
      </header>
      <div className="pages-nav">
        <div className="links">
          <a className="active" href="">
            Resources
          </a>
          <a href="">IAM Policy</a>
        </div>
        <div className="search-container">
          <div className="search-bar">
            <input
              type="text"
              name="search-input"
              id="search-input"
              placeholder="Resource Name"
            />
            <IconButton sx={{p: '0', color: '#3367D6'}} aria-label="search">
              <SearchIcon />
            </IconButton>
          </div>
        </div>
      </div>
    </>
  );
};

export default Navbar;
