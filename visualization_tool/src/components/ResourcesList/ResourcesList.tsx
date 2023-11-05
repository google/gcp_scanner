import { useState } from 'react';
import { Resource } from '../../types/resources';
import { typeToImage, statusToColor } from './utils';
import { useFilter } from './useFilter';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
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

  const [isGridView, setIsGridView] = useState<boolean>(true);

  return (
    <div className="resources-list">
      <div className="header-container">
        <h1 className='header-text'>{resources.length > 0 ? 'Found Resources' : 'No Resources Found'}</h1>
        <div className="button-container">
          <button className={isGridView ? 'active' : ''} onClick={() => { setIsGridView(true) }}>
            <span>
              <img src="./icons/grid.png" alt="" className="icon" />
            </span>
            <h4>Grid View</h4>
          </button>
          <button className={!isGridView ? 'active' : ''} onClick={() => { setIsGridView(false) }}>
            <span>
              <img src="./icons/list.png" alt="" className="icon" />
            </span>
            <h4>List View</h4>
          </button>
        </div>
      </div>
      <Details
        selectedResource={selectedResource}
        openDetails={openDetails}
        setOpenDetails={setOpenDetails}
      />
      {isGridView ?
        <div className="resources-list__table">
          {filteredResources.map((resource) => (
            <div
              className="resources-list__table__card"
              key={resource.id ? resource.id : resource.name}
            >
              <p className="resource-name">{resource.name}</p>
              <div className="resource-type_container">
                <img src={typeToImage(resource)} className="resources-image" />
                <p className="resource-type">{resource.type}</p>
              </div>
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
          ))}
        </div>
        :
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell></TableCell>
                <TableCell>Resource Type</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredResources.map((resource) => (
                <TableRow key={resource.id ? resource.id : resource.name} >
                  <TableCell><img src={typeToImage(resource)} className="resources-image" /></TableCell>
                  <TableCell>{resource.type}</TableCell>
                  <TableCell>{resource.name}</TableCell>
                  <TableCell><p
                    style={{
                      color: statusToColor(resource.status),
                    }}
                  >
                    {resource.status}
                  </p></TableCell>
                  <TableCell className='table-button'>
                    <button
                      onClick={() => {
                        setSelectedResource(resource);
                        setOpenDetails(true);
                      }}
                    >
                      Details
                    </button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      }

    </div>
  );
};

export default ResourcesList;
