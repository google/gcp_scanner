import {useEffect, useState} from 'react';
import {Resource} from '../../types/resources';
import {debounce} from '@mui/material';

export const useFilter = (resources: Resource[], searchQuery: string) => {
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
            return (
              new Date(a.creationTimestamp).getTime() -
              new Date(b.creationTimestamp).getTime()
            );
          })
      );
    };

    debounce(filterResources, 100)();
  }, [resources, searchQuery]);

  return filteredResources;
};
