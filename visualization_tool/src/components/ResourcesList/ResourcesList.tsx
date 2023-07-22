import {Resource} from '../../types/resources';
import {typeToImage, statusToColor} from './utils';
import {useFilter} from './useFilter';

import './ResourcesList.css';

type ResourcesListProps = {resources: Resource[]; searchQuery: string};

const ResourcesList = ({resources, searchQuery}: ResourcesListProps) => {
  const filteredResources = useFilter(resources, searchQuery);
  return (
    <div className="resources-list">
      <h1>{resources.length > 0 ? 'Found Resources' : 'No Resources Found'}</h1>
      <div className="resources-list__table">
        {filteredResources.map(resource => {
          return (
            <div className="resources-list__table__card" key={resource.id}>
              <img src={typeToImage(resource)} alt="" />
              <p className="resource-name">{resource.name}</p>
              <p className="resource-type">{resource.type}</p>
              <p
                className="resource-status"
                style={{
                  color: statusToColor(resource.status),
                }}
              >
                {resource.status}
              </p>
              <button>Details</button>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ResourcesList;
