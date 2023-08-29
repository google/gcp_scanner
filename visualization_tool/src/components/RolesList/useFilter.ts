import {useEffect, useState} from 'react';
import {IAMRole} from '../../types/IAMPolicy';
import {debounce} from '@mui/material';

export const useFilter = (roles: IAMRole[], email: string) => {
  const [filteredRoles, setFilteredRoles] = useState<IAMRole[]>(roles);

  useEffect(() => {
    const filterRoles = () => {
      setFilteredRoles(
        roles.filter(role => {
          // check if this email is in the role's members
          return role.members.some(member => member.email.includes(email));
        })
      );
    };

    debounce(filterRoles, 200)();
  }, [roles, email]);

  return filteredRoles;
};
