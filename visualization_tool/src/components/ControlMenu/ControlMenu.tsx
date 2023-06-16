import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';

import './ControlMenu.css';

const ControlMenu = () => {
  return (
    <div className="control-menu">
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
  );
};

export default ControlMenu;
