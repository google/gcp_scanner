import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Row from './partials/Row';
import {IAMRole} from '../../types/IMAPolicy';

import './RolesList.css';

type RolesListProps = {
  roles: IAMRole[];
};

const RolesList = ({roles}: RolesListProps) => {
  return (
    <div className="roles-list">
      <h1>{roles.length > 0 ? 'Found Roles' : 'No Roles Found'}</h1>
      {roles.length > 0 && (
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
              {roles.map(role => (
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
