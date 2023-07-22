import {useEffect} from 'react';
import IconButton from '@mui/material/IconButton';
import {KeyboardCommandKey} from '@mui/icons-material';

import './Navbar.css';
import logo from '/logo.png';

type NavbarProps = {
  searchQuery: string;
  setSearchQuery: React.Dispatch<React.SetStateAction<string>>;
};

const Navbar = ({searchQuery, setSearchQuery}: NavbarProps) => {
  useEffect(() => {
    const searchInput = document.getElementById(
      'search-input'
    ) as HTMLInputElement;
    // autofocus on search input
    searchInput.focus();
    // focus on search input with ctrl + f
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.key === 'f') {
        e.preventDefault();
        searchInput.focus();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

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
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
            />

            <IconButton
              sx={{p: '0', color: '#3367D6', fontSize: '18px'}}
              aria-label="search"
            >
              <KeyboardCommandKey />+ f
            </IconButton>
          </div>
        </div>
      </div>
    </>
  );
};

export default Navbar;
