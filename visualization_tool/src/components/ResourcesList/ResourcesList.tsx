import {useState} from 'react';
import {Resource} from '../../types/resources';
import {typeToImage, statusToColor} from './utils';
import {useFilter} from './useFilter';
import Details from './partials/Detalis';

import './ResourcesList.css';

type ResourcesListProps = {
  resources: Resource[];
  searchQuery: string;
  sortAttribute: string;
  allowedTypes: string[];
  allowedProjects: string[];
};

const ResourcesList = ({
  resources,
  searchQuery,
  sortAttribute,
  allowedTypes,
  allowedProjects,
}: ResourcesListProps) => {
  const filteredResources = useFilter(
    resources,
    searchQuery,
    sortAttribute,
    allowedTypes,
    allowedProjects
  );
  const [selectedResource, setSelectedResource] = useState<Resource | null>(
    null
  );
  const [openDetails, setOpenDetails] = useState<boolean>(false);
  return (
    <div className="resources-list">
      <h1>{resources.length > 0 ? 'Found Resources' : 'No Resources Found'}</h1>
      <Details
        selectedResource={selectedResource}
        openDetails={openDetails}
        setOpenDetails={setOpenDetails}
      />
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
              <button
                onClick={() => {
                  setSelectedResource(resource);
                  setOpenDetails(true);
                }}
              >
                Details
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ResourcesList;
