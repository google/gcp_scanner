import {useEffect} from 'react';
import {Link, useLocation} from 'react-router-dom';
import IconButton from '@mui/material/IconButton';
import {KeyboardCommandKey} from '@mui/icons-material';

import './Navbar.css';
import logo from '/logo.png';

type NavbarProps = {
  searchQuery: string;
  setSearchQuery: React.Dispatch<React.SetStateAction<string>>;
};

const Navbar = ({searchQuery, setSearchQuery}: NavbarProps) => {
  const location = useLocation();
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
        <p>GCP Scanner</p>
      </header>
      <div className="pages-nav">
        <div className="links">
          <Link
            to="/static/"
            className={location.pathname === '/static/' ? 'active' : ''}
            onClick={() => {
              setSearchQuery('');
            }}
          >
            Resources
          </Link>
          <Link
            to="/static/iam-policy"
            className={
              location.pathname === '/static/iam-policy' ? 'active' : ''
            }
            onClick={() => {
              setSearchQuery('');
            }}
          >
            IAM Policy
          </Link>
        </div>
        <div className="search-container">
          <div className="search-bar">
            <input
              type="text"
              name="search-input"
              id="search-input"
              placeholder="Search"
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
