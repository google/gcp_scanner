import {useLocation} from 'react-router-dom';

import UploadMenu from './partials/UploadMenu';
import SortMenu from './partials/SortMenu';
import FilterMenu from './partials/FilterMenu';

import {Resource} from '../../types/resources';

type ControlMenuProps = {
  setResources: React.Dispatch<React.SetStateAction<Resource[]>>;
  setSortAttribute: React.Dispatch<React.SetStateAction<string>>;
  setAllowedTypes: React.Dispatch<React.SetStateAction<string[]>>;
};

const ControlMenu = ({
  setResources,
  setSortAttribute,
  setAllowedTypes,
}: ControlMenuProps) => {
  const location = useLocation();

  return (
    <div>
      <UploadMenu setResources={setResources} />
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
