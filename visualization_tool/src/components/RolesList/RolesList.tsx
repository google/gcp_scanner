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
  allowedProjects: string[];
};

const RolesList = ({roles, emailQuery, allowedProjects}: RolesListProps) => {
  const filteredRoles = useFilter(roles, emailQuery, allowedProjects);
  const projects = [...new Set(roles.map(role => role.projectId))];

  return (
    <div className="roles-list">
      <h1>{roles.length > 0 ? 'Found Roles' : 'No Roles Found'}</h1>
      {filteredRoles.length > 0 && (
        <TableContainer component={Paper}>
          <Table aria-label="collapsible table" size="small">
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
                    fontSize: '1.1rem',
                  }}
                >
                  Role
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {
                // create a outer cell for each project
                projects.map(project => {
                  // filter roles by project
                  const projectRoles = filteredRoles.filter(
                    role => role.projectId === project
                  );
                  return (
                    <>
                      <TableRow
                        sx={{
                          backgroundColor: '#f5f5f5',
                        }}
                        key={project}
                      >
                        <TableCell
                          sx={{
                            width: '10px',
                            padding: '0px',
                          }}
                        />
                        <TableCell
                          sx={{
                            fontWeight: 'bold',
                            fontSize: '1.05rem',
                          }}
                        >
                          {project}
                        </TableCell>
                      </TableRow>
                      {
                        // create a row for each role
                        projectRoles.map(role => (
                          <Row key={`${role.role}__${project}`} row={role} />
                        ))
                      }
                    </>
                  );
                })
              }
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </div>
  );
};

export default RolesList;
