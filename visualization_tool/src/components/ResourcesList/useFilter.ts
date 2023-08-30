import {useEffect, useState} from 'react';
import {Resource} from '../../types/resources';
import {debounce} from '@mui/material';

export const useFilter = (
  resources: Resource[],
  searchQuery: string,
  sortAttribute: string,
  allowedTypes: string[],
  allowedProjects: string[]
) => {
  const [filteredResources, setFilteredResources] =
    useState<Resource[]>(resources);

  useEffect(() => {
    const filterResources = () => {
      setFilteredResources(
        resources
          .filter(resource => {
            return (
              allowedTypes.includes(resource.type) &&
              resource.name.toLowerCase().includes(searchQuery.toLowerCase()) &&
              allowedProjects.includes(resource.projectId)
            );
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
  }, [resources, searchQuery, sortAttribute, allowedTypes, allowedProjects]);

  return filteredResources;
};
