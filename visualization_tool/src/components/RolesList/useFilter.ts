import {useEffect, useState} from 'react';
import {IAMRole} from '../../types/IAMPolicy';
import {debounce} from '@mui/material';

export const useFilter = (
  roles: IAMRole[],
  email: string,
  allowedProjects: string[]
) => {
  const [filteredRoles, setFilteredRoles] = useState<IAMRole[]>(roles);

  useEffect(() => {
    const filterRoles = () => {
      setFilteredRoles(
        roles.filter(role => {
          return (
            role.members.some(member => member.email.includes(email)) &&
            allowedProjects.includes(role.projectId)
          );
        })
      );
    };

    debounce(filterRoles, 200)();
  }, [roles, email, allowedProjects]);

  return filteredRoles;
};
