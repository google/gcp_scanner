import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Row from './partials/Row';

import {IAMRole} from '../../types/IAMPolicy';
import {useFilter} from './useFilter';

import './RolesList.css';

type RolesListProps = {
  roles: IAMRole[];
  emailQuery: string;
};

const RolesList = ({roles, emailQuery}: RolesListProps) => {
  const filteredRoles = useFilter(roles, emailQuery);
  // console.log(filteredRoles);

  return (
    <div className="roles-list">
      <h1>{roles.length > 0 ? 'Found Roles' : 'No Roles Found'}</h1>
      {filteredRoles.length > 0 && (
        <TableContainer component={Paper}>
          <Table aria-label="collapsible table">
            <TableHead>
              <TableRow>
                <TableCell
                  sx={{
                    width: '10px',
                    padding: '0px',
                  }}
                />
                <TableCell
                  sx={{
                    fontWeight: 'bold',
                    fontSize: '1rem',
                  }}
                >
                  Role
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredRoles.map(role => (
                <Row key={role.role} row={role} />
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </div>
  );
};

export default RolesList;
