import {useLocation} from 'react-router-dom';

import UploadMenu from './partials/UploadMenu';
import SortMenu from './partials/SortMenu';
import FilterMenu from './partials/FilterMenu';

import {Resource} from '../../types/resources';
import {IAMRole} from '../../types/IMAPolicy';

type ControlMenuProps = {
  setResources: React.Dispatch<React.SetStateAction<Resource[]>>;
  setSortAttribute: React.Dispatch<React.SetStateAction<string>>;
  setAllowedTypes: React.Dispatch<React.SetStateAction<string[]>>;
  setRoles: React.Dispatch<React.SetStateAction<IAMRole[]>>;
};

const ControlMenu = ({
  setResources,
  setSortAttribute,
  setAllowedTypes,
  setRoles,
}: ControlMenuProps) => {
  const location = useLocation();

  return (
    <div>
      <UploadMenu setResources={setResources} setRoles={setRoles} />
      {location.pathname === '/static/' && (
        <>
          <SortMenu setSortAttribute={setSortAttribute} />
          <FilterMenu setAllowedTypes={setAllowedTypes} />
        </>
      )}
    </div>
  );
};

export default ControlMenu;
