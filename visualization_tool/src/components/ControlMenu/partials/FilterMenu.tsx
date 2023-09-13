import {availableResourceTypes} from '../../../types/resources';

type FilterMenuProps = {
  setAllowedTypes: React.Dispatch<React.SetStateAction<string[]>>;
};

const FilterMenu = ({setAllowedTypes}: FilterMenuProps) => {
  return (
    <div className="menu-item">
      <div className="menu-item__header">
        <span>
          <img src="./icons/filter.png" alt="" />
        </span>
        <h3>Resource Type</h3>
      </div>
      {availableResourceTypes.length > 0 && (
        <div className="menu-item__content">
          {availableResourceTypes.map(type => {
            return (
              <div key={type}>
                <input
                  type="checkbox"
                  name="resource-type"
                  id={type}
                  defaultChecked
                  onChange={e => {
                    if (e.target.checked) {
                      setAllowedTypes(prevTypes => [...prevTypes, type]);
                    } else {
                      setAllowedTypes(prevTypes => {
                        return prevTypes.filter(prevType => prevType !== type);
                      });
                    }
                  }}
                />
                <label htmlFor={type}>{type}</label>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default FilterMenu;
