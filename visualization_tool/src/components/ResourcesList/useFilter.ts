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
      let filtered = resources.filter(resource => {
        return (
          allowedTypes.includes(resource.type) &&
          allowedProjects.includes(resource.projectId)
        );
      });

      if (searchQuery.trim() !== '') {
        try {
          const regex = new RegExp(searchQuery, 'i');
          filtered = filtered.filter(resource => regex.test(resource.name));
        } catch (error) {
          // If the RegExp constructor throws an error, do a normal search
          filtered = filtered.filter(resource =>
            resource.name.toLowerCase().includes(searchQuery.toLowerCase())
          );
        }
      }

      filtered.sort((a, b) => {
        if (sortAttribute === 'name') {
          return a.name.localeCompare(b.name);
        } else {
          return (
            new Date(a.creationTimestamp).getTime() -
            new Date(b.creationTimestamp).getTime()
          );
        }
      });

      setFilteredResources(filtered);
    };

    debounce(filterResources, 100)();
  }, [resources, searchQuery, sortAttribute, allowedTypes, allowedProjects]);

  return filteredResources;
};
