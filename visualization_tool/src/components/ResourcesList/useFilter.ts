import {useEffect, useState} from 'react';
import {Resource} from '../../types/resources';
import {debounce} from '@mui/material';

export const useFilter = (
  resources: Resource[],
  searchQuery: string,
  sortAttribute: string
) => {
  const [filteredResources, setFilteredResources] =
    useState<Resource[]>(resources);

  useEffect(() => {
    const filterResources = () => {
      setFilteredResources(
        resources
          .filter(resource => {
            return resource.name
              .toLowerCase()
              .includes(searchQuery.toLowerCase());
          })
          .sort((a, b) => {
            if (sortAttribute === 'name') {
              return a.name.localeCompare(b.name);
            } else {
              return (
                new Date(a.creationTimestamp).getTime() -
                new Date(b.creationTimestamp).getTime()
              );
            }
          })
      );
    };

    debounce(filterResources, 100)();
  }, [resources, searchQuery, sortAttribute]);

  return filteredResources;
};
