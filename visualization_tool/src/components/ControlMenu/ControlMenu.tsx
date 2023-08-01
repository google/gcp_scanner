import UploadMenu from './partials/UploadMenu';
import SortMenu from './partials/SortMenu';
import FilterMenu from './partials/FilterMenu';

import {Resource} from '../../types/resources';

import './ControlMenu.css';

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
  return (
    <div className="control-menu">
      <UploadMenu setResources={setResources} />
      <SortMenu setSortAttribute={setSortAttribute} />
      <FilterMenu setAllowedTypes={setAllowedTypes} />
    </div>
  );
};

export default ControlMenu;
