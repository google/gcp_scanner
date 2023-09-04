import {useLocation} from 'react-router-dom';

import UploadMenu from './partials/UploadMenu';
import SortMenu from './partials/SortMenu';
import FilterMenu from './partials/FilterMenu';
import FilterProjects from './partials/FilterProjects';

import {Resource} from '../../types/resources';
import {IAMRole} from '../../types/IAMPolicy';

import './ControlMenu.css';

type ControlMenuProps = {
  setResources: React.Dispatch<React.SetStateAction<Resource[]>>;
  setSortAttribute: React.Dispatch<React.SetStateAction<string>>;
  setAllowedTypes: React.Dispatch<React.SetStateAction<string[]>>;
  setRoles: React.Dispatch<React.SetStateAction<IAMRole[]>>;
  projects: string[];
  setProjects: React.Dispatch<React.SetStateAction<string[]>>;
  setAllowedProjects: React.Dispatch<React.SetStateAction<string[]>>;
};

const ControlMenu = ({
  setResources,
  setSortAttribute,
  setAllowedTypes,
  setRoles,
  projects,
  setProjects,
  setAllowedProjects,
}: ControlMenuProps) => {
  const location = useLocation();

  return (
    <div className="control-menu-container">
      <div className="control-menu">
        <UploadMenu
          setResources={setResources}
          setRoles={setRoles}
          setProjects={setProjects}
          setAllowedProjects={setAllowedProjects}
        />
        <FilterProjects
          projects={projects}
          setAllowedProjects={setAllowedProjects}
        />
        {location.pathname === '/' && (
          <>
            <SortMenu setSortAttribute={setSortAttribute} />
            <FilterMenu setAllowedTypes={setAllowedTypes} />
          </>
        )}
      </div>
    </div>
  );
};

export default ControlMenu;
