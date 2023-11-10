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
      let filtered = roles.filter(role => {
        return allowedProjects.includes(role.projectId);
      });

      if (email.trim() !== '') {
        try {
          const regex = new RegExp(email, 'i');
          filtered = filtered.filter(role =>
            role.members.some(member => regex.test(member.email))
          );
        } catch (error) {
          // If the RegExp constructor throws an error, do a normal search
          filtered = filtered.filter(role =>
            role.members.some(member =>
              member.email.toLowerCase().includes(email.toLowerCase())
            )
          );
        }
      }

      setFilteredRoles(filtered);
    };

    debounce(filterRoles, 200)();
  }, [roles, email, allowedProjects]);

  return filteredRoles;
};
